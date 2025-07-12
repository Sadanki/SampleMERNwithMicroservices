FROM node:16

# Create app directory
WORKDIR /usr/src/app

# Copy and install app dependencies
COPY package*.json ./
RUN npm install

# Copy app source code
COPY . .

# Create .env file
RUN echo "PORT=3000" > .env

# Expose port
EXPOSE 3000

# Start the app
CMD [ "node", "index.js" ]