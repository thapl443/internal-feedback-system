# Use Node 20 for compatibility with latest Vite
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose Vite port
EXPOSE 5173

# Run in dev mode for the demo
CMD ["npm", "run", "dev", "--", "--host"]
