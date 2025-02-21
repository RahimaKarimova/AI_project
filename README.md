# Hotel Room Booking System

## Project Overview
The **Hotel Room Booking System** is an AI-based solution designed to efficiently assign rooms to hotel bookings while satisfying multiple constraints such as room capacity, availability, and user preferences. The project applies **Constraint Satisfaction Problem (CSP)** techniques to ensure optimal scheduling and customer satisfaction.

## Problem Statement
The primary goal of this project is to develop an intelligent booking system that efficiently allocates rooms based on a combination of hard and soft constraints:
- **Hard Constraints**: Room capacity, availability
- **Soft Constraints**: Floor preferences, room type preferences

By leveraging CSP techniques, the system enhances room assignment efficiency while maximizing customer satisfaction.

## Data
- The dataset is provided in **JSON format**.
- It includes **dozens of bookings** and room details.
- Key attributes:
  - Room capacity
  - Availability
  - Floor preferences
  - Room types

## Algorithms & Techniques
The system uses **Backtracking Search** combined with constraint heuristics to optimize scheduling.

### **Backtracking Algorithm**
- Explores all possible room-booking assignments.
- Uses pruning to eliminate infeasible options efficiently.

### **Heuristics**
- **MRV (Minimum Remaining Values)**: Prioritizes bookings with the least room options available.
- **LCV (Least Constraining Value)**: Maximizes flexibility for future assignments.
- **Forward Checking**: Ensures constraint propagation to improve efficiency.

### **Modular Design**
- Encapsulation using **Room** and **Booking** classes to maintain clarity and scalability.

## Results
- Successfully scheduled **185 out of 200 bookings** (**92.5% success rate**).
- Failures were primarily due to insufficient room capacity or unavailability.
- The system effectively optimized the fulfillment of **soft constraints** (e.g., floor preferences).

## Considerations & Future Enhancements
### **Computational Challenges**
- High search space was tackled using **constraints and heuristics (MRV, LCV)**.
- Early termination techniques reduced excessive computations while maintaining quality results.

### **Scalability**
- Works efficiently for moderate-sized datasets.
- Future iterations may require **more advanced optimization techniques** for larger datasets.

### **Future Enhancements**
- Enhanced **constraint modeling** to handle dynamic real-world booking scenarios.
- **Improved data preprocessing** for better performance and efficiency.

## Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RahimaKarimova/AI_project.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd AI_project
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the program:**
   ```bash
   python main.py
   ```

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
### **Thank You for Your Attention!**
