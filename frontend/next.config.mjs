/** @type {import('next').NextConfig} */

const nextConfig = {
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8081/:path*', // Proxy to Backend
        },
      ]
    },
  }
  
// module.exports = nextConfig
export default nextConfig;
