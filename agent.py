import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=9000)
        self.max_memory_size = 8400
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.max_memory_size-1:
            self.prune_memory(1500)  # Prune the oldest 1500 experiences

    def prune_memory(self, num_to_prune):
        # Remove the oldest experiences from memory
        for _ in range(num_to_prune):
            if self.memory:
                self.memory.popleft()

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model(torch.FloatTensor(state))
        return torch.argmax(act_values).item()

    def replay(self, batch_size):
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        minibatch = random.sample(self.memory, batch_size)
        
        # Store states and targets for the batch
        states = []
        targets = []
        
        for state, action, reward, next_state, done in minibatch:
            if state is None or next_state is None:
                continue  # Skip if state is None
            target = reward
            if not done:
                target += self.gamma * torch.max(self.model(torch.FloatTensor(next_state))).item()
            
            # Store the state and target
            states.append(state)
            target_f = self.model(torch.FloatTensor(state)).detach()  # Get the model's prediction
            target_f[action] = target  # Update the action's value
            targets.append(target_f)

        # Convert lists to tensors
        states = torch.FloatTensor(states)
        targets = torch.stack(targets)

        # Compute loss and optimize
        self.model.zero_grad()
        loss = nn.MSELoss()(self.model(states), targets)  # Compare model predictions with targets
        loss.backward()
        optimizer.step()

            
    def load_model(self, file_path):
        self.model.load_state_dict(torch.load(file_path))  # Load the model state dict
        self.model.eval()  # Set the model to evaluation mode
        print(f'Model loaded from {file_path}')

    def save_model(self, file_path):
        torch.save(self.model.state_dict(), file_path)  # Save the model state dict
        print(f'Model saved to {file_path}')
