import { create } from 'zustand';
import { useEffect, useRef } from 'react';

interface DetectionState {
  ear: number;
  mar: number;
  fatigue_prob: number;
  state: 'ALERT' | 'CAUTION' | 'DROWSY' | 'UNKNOWN';
  blink_count: number;
  yawn_count: number;
  fps: number;
  bbox: number[];
  landmarks: number[][];
  isConnected: boolean;
  setConnected: (status: boolean) => void;
  updateDetection: (data: Partial<DetectionState>) => void;
  sendFrame: (base64: string) => void;
}

export const useDetectionStore = create<DetectionState>((set) => ({
  ear: 0,
  mar: 0,
  fatigue_prob: 0,
  state: 'ALERT',
  blink_count: 0,
  yawn_count: 0,
  fps: 0,
  bbox: [],
  landmarks: [],
  isConnected: false,
  setConnected: (status) => set({ isConnected: status }),
  updateDetection: (data) => set((state) => ({ ...state, ...data })),
  sendFrame: (base64: string) => {
    // This is a placeholder, the actual sending logic is in the hook below
  },
}));

// Set EXPO_PUBLIC_BACKEND_HOST to the computer's LAN IP when using a physical device.
const BACKEND_HOST = process.env.EXPO_PUBLIC_BACKEND_HOST || 'localhost';
const WS_URL = `ws://${BACKEND_HOST}:8765/detection`; 

console.log('Connecting to WebSocket at:', WS_URL);

export const useDetection = () => {
  const store = useDetectionStore();
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    let reconnectDelay = 1000;

    const connect = () => {
      ws.current = new WebSocket(WS_URL);

      ws.current.onopen = () => {
        store.setConnected(true);
        reconnectDelay = 1000; // reset
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          store.updateDetection(data);
        } catch (e) {
          console.error("Error parsing detection data", e);
        }
      };

      ws.current.onclose = () => {
        store.setConnected(false);
        // Reconnect with exponential backoff
        timeoutId = setTimeout(() => {
          reconnectDelay = Math.min(reconnectDelay * 2, 30000);
          connect();
        }, reconnectDelay);
      };
    };

    connect();

    return () => {
      clearTimeout(timeoutId);
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  const sendFrame = (base64: string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ frame: base64 }));
    }
  };

  return { ...store, sendFrame };
};
