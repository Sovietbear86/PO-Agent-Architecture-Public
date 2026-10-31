import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Public deployments may run alongside an existing Review stack.
// Accept only loopback proxy destinations; never proxy browser /api to remote hosts.
const agentPort = Number(process.env.PO_AGENT_DEV_PROXY_PORT || '8004')
const vitePort = Number(process.env.PO_AGENT_DEV_UI_PORT || '5175')
const validPort = (port: number) => Number.isInteger(port) && port >= 1024 && port <= 65535
if (!validPort(agentPort) || !validPort(vitePort)) {
  throw new Error('PO_AGENT_DEV_PROXY_PORT and PO_AGENT_DEV_UI_PORT must be valid unprivileged TCP ports')
}

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: vitePort,
    strictPort: true,
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${agentPort}`,
        changeOrigin: true,
      },
    },
  },
})
