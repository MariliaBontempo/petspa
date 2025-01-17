FROM node:18-alpine

WORKDIR /app

# Usar yarn em vez de npm
COPY package.json yarn.lock ./
RUN yarn install

COPY . .

EXPOSE 3000

# Comando para Vite
CMD ["yarn", "dev", "--host"] 