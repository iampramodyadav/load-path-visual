# Car Suspension System Model

This JSON file models a front suspension system for a vehicle, demonstrating the load paths between various components. The model can be visualized and analyzed using the Load Path Visual Tool.

## Components

1. **Chassis** - The main body structure of the vehicle
2. **Upper Control Arm** - Connects the chassis to the steering knuckle
3. **Lower Control Arm** - Connects the chassis to the steering knuckle
4. **Steering Knuckle** - Central component that connects the wheel, control arms, and tie rod
5. **Tie Rod** - Connects the steering rack to the steering knuckle
6. **Steering Rack** - Translates rotational motion to linear motion for steering
7. **Shock Absorber** - Dampens oscillations and absorbs energy from impacts
8. **Wheel** - Transfers vehicle load to the ground and provides traction
9. **Ground** - The contact surface for the wheel

## Load Paths

The model shows how forces are transferred through the suspension system:

- Chassis → Upper and Lower Control Arms → Steering Knuckle → Wheel → Ground
- Chassis → Steering Rack → Tie Rod → Steering Knuckle
- Chassis → Shock Absorber → Lower Control Arm

## Forces and Moments

- Vehicle weight (gravity) is applied to all mass components
- Ground reaction force applied at the wheel (3000N vertical)
- Force transfer through joints with appropriate moments
- All connections have valid RLT (Rigid Load Transfer) results

## Coordinate System

- Right-handed coordinate system
- Units: force (N), moment (Nm), mass (kg), distance (mm)
- Gravity direction: [0, 0, -1] with magnitude 9.81 m/s²

## Visualization

Import this JSON file into the Load Path Visual Tool to see the graphical representation of the suspension system and analyze the load paths between components. 