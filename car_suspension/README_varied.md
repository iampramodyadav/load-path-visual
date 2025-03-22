# Car Suspension System Model with Varied Coordinate Information

This JSON file models a front suspension system for a vehicle with realistic coordinate transformations. It provides a more detailed representation of component orientations and connection interfaces than the basic model.

## Coordinate Transformation Features

- **Varied Euler Angles**: Each component has specific rotation angles in degrees
- **Different Rotation Orders**: Uses multiple rotation conventions (xyz, zyx, xzy, yxz, etc.)
- **Offset Positions**: Connection points have realistic offsets from perfect alignment
- **Realistic Interface Properties**: Each connection specifies precise position and orientation

## Components

1. **Chassis** (zyx rotation) - The main body structure with subtle pitch and roll orientations
2. **Upper Control Arm** (xyz rotation) - Pronounced camber angle (12.5° about Y axis)
3. **Lower Control Arm** (xyz rotation) - Negative camber angle (-8.3° about Y) with slight twist
4. **Steering Knuckle** (xzy rotation) - Complex orientation with roll and yaw angles
5. **Tie Rod** (zxy rotation) - Slight rotational offset for steering alignment
6. **Steering Rack** (yxz rotation) - Pitch angle of 3.7° about Y axis
7. **Shock Absorber** (zyx rotation) - Significant 35.2° rotation about Z axis
8. **Wheel** (zxy rotation) - 85.3° rotation about Z for wheel spin orientation
9. **Ground** (xyz rotation) - Standard horizontal reference plane

## Connection Interfaces

Each edge in the model features:

- Custom interface position with mm-level offsets from nominal positions
- Specific Euler angles for connection orientation
- Varied rotation orders appropriate for each mechanical interface
- Valid force and moment transfer values

## Sample Connections

- **Chassis → Upper Control Arm**: Rotation order "yzx" with position offset [12, -105, 465]
- **LowerControlArm → SteeringKnuckle**: Rotation order "yxz" with position [-5, -402, 298]
- **TieRod → SteeringKnuckle**: 8.7° rotation about Z with "zxy" rotation order

## Visualization and Analysis

This model provides a significantly more realistic representation of a suspension system's 3D geometry compared to the basic model. When visualized, it will show the true spatial relationships between components with proper orientations.

Import this JSON file into the Load Path Visual Tool to see the precise spatial representation of the suspension system and analyze the load paths in a realistic 3D configuration. 