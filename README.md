# 🚒 FireFighterBot 🔥

FireFighterBot is an innovative robotics project created to compete in the **Trinity Firefighting Competition**. This competition challenges teams to design robots that autonomously locate and extinguish flames while navigating a dynamic obstacle course. My project stands out by integrating a **Deep Q-Network (DQN)** reinforcement learning (RL) agent, allowing the bot to learn and adapt through trial and error—an approach rarely seen in this competition.

---

## 🛠️ Features

### 🔥 Autonomous Fire Detection and Extinguishing
- **Flame Sensor**: Detects the presence and direction of flames.
- **Obstacle Navigation**: Three ultrasonic sensors simulate raycasts for precise navigation and obstacle avoidance.

### ⚙️ Precision Movement
- **Motor Encoders & Servos**: Ensure accurate turns and movement.
- **DQN Agent**: Learns optimal strategies for:
  - Turning
  - Moving forward
  - Adjusting the flame sensor

### 🤖 Reinforcement Learning Approach
My use of reinforcement learning is a **novel approach** in the Trinity Firefighting Competition. While traditional bots rely on pre-programmed logic, my bot interacts with its environment in real-time. The DQN agent:
- Observes its state (obstacles, flame sensor angle, flame detection).
- Takes actions to maximize rewards (e.g., extinguishing a flame).
- Learns through penalties (e.g., crashing) and rewards.

This results in **adaptive behavior** that optimizes performance over time, handling scenarios that pre-programmed logic might fail to address.

---

## 🔄 Adaptive Learning
- **Reward System**: Encourages successful flame extinguishing and penalizes errors.
- **PyTorch Training**: A flexible library for reinforcement learning, enabling continuous improvement.

---

## 🧠 Why Reinforcement Learning?
Using RL offers key advantages:
- **Autonomy**: Learns actions without explicit instructions.
- **Optimization**: Improves performance with experience.
- **Flexibility**: Adapts to changing environments without reprogramming.
- **Real-World Applicability**: Demonstrates AI’s role in solving dynamic problems, akin to autonomous vehicles.

---

## 🚀 Hardware Overview

### **Core Components**
- **ESP32**: Handles sensor data, DQN processing, and motor control.
- **Flame Sensor**: Detects and locates flames.
- **Ultrasonic Sensors**: Aid in obstacle detection and navigation.
- **Servo Motors**: Control movement and flame sensor adjustments.
- **Motors with Encoders**: Ensure precise movement and tracking.

### **Learning Environment**
A simulated training environment mirrors the competition field, enabling the bot to refine its actions and optimize flame extinguishing while navigating obstacles.

---

## 📚 Resources
- [Trinity Firefighting Competition](https://www.facebook.com/trinityrobotcontest/)
- [PyTorch](https://pytorch.org)
- [ESP32](https://www.espressif.com/en/products/socs/esp32)

---

FireFighterBot showcases how **AI-driven robotics** can revolutionize dynamic problem-solving. By merging reinforcement learning with robotics, this project highlights the future of autonomous systems! 🔥🤖
