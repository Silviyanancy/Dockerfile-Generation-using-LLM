# Here is a Dockerfile for your project that sets up a Node.js environment and installs the necessary dependencies:


# Use an official Node runtime as a parent image
FROM node:latest

# Set working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install dependencies using npm
RUN npm install

# Copy all other application files into the container
COPY . ./

# Expose port 3000 for the app
EXPOSE 3000

# Define the command to run when the container starts
CMD ["npm", "start"]
