# ̽������Ϸ - README

## ��Ϸ���
����һ�����Pygame������̽����������Ϸ����ҽ�����̽�����ڵ�ͼ���ռ�ʳ���ȡ������ͬʱ���������ߵ�׷������Ϸ�ں��˶�̬����ϵͳ�����������AI׷�ٻ��ƣ��������в����Ե��������顣

## ���ϵͳ���

### ��������
- **����ϵͳ**����ʼ����ֵΪ`PLAYER_INIT_ENERGY`���������ֵΪ400����������ʱ����Ȼ���ģ�Ҳ�����ƶ��ͳ�̶�������
- **���ͱ仯**����������ֵ��̬�ı��С
  - ����=0ʱ���������ͣ�1�������뾶��
  - ����=200ʱ��2�������뾶
  - ����=400ʱ��3�������뾶
- **�ٶ�����**���������ɷ��ȹ�ϵ
  - ����=0ʱ��150%�����ٶ�
  - ����=200ʱ��75%�����ٶ�
  - ����=400ʱ��50%�����ٶ�

### ��������
- **�ƶ�����**��ͨ������������ǰ������ɫ���Զ��������ָ�뷽����ת
- **��̹���**������Ҽ�����������20����������ʱ���ڴ�������ƶ��ٶȣ�`PLAYER_DASH_SPEED_MULTIPLIER`����
- **�����ָ�**��ͨ���ռ�ʳ��������������ͬ��ֵ��ʳ���ṩ��ͬ����ֵ

### �Ӿ�����
- ǳ��ɫԲ�����壬���ʱ��ɫ����
- ����ת����仯���۾�����ͣ���ǿ��ɫ������
- ͷ��������ֱ����ʾ��ǰ����״̬����ɫ����ɫ����ɫ���䣩
- ���ʱ�����°�͸���켣��������������

## ��Ŀ�ṹ
������ main.py # ������ڣ�������ť��Ϳ�ʼ����
������ game.py # ��Ϸ���߼���������Ϸѭ���ͺ��Ļ���
������ player.py # ����࣬�����ƶ�����ת�������ͻ���
������ map.py # ��ͼ��С��ͼ�����������߼�
������ food.py # ʳ��ʵ����
������ hunter.py # ������ AI ��
������ audio.py # ��Ƶ����ϵͳ
������ audio/ # ��Ƶ��ԴĿ¼
������ eat.mp3 # ��ʳ����Ч
������ lost.mp3 # ��Ϸʧ����Ч
������ run.mp3 # �����Ч
������ win.mp3 # ��Ϸʤ����Ч

## ����ģ��˵��

### 1. ��Ƶϵͳ��audio.py��
- **AudioManager��**�����ڶ����ģʽ����Ƶ����ϵͳ
  - ��ʼ�����Զ���Ⲣ��ʼ��Pygame��Ƶϵͳ��֧���Զ�����С/���ʵ����
  - ��Ч���أ��Զ�����`audio`Ŀ¼�µĻ�����Ч��eat/lost/run/win����ȱʧ�ļ�ʱ��������
  - �������ƣ��ṩ`set_volume()`��`get_volume()`������֧��ȫ���������ڣ�0.0-1.0��Χ��
  - ʵ������
    - ��̬ά����Чʵ���أ��Զ���������ɲ��ŵ�ʵ��
    - ֧��ͬʱ���Ŷ����ͬ��Ч�����������ʵ�������ƣ�
    - �Զ���������С�������Ŀ���ʵ�����Ż���Դռ��
  - ���ſ��ƣ�`play_sound()`����ָ����Ч��`stop_sound()`ֹͣ�ض���Ч����ʵ����`clear_all()`ֹͣ������Ч

### 2. ��Ϸ���ģ�game.py��
- ������Ϸ��ѭ����״̬���ºͻ�����Ⱦ
- ������ײ��⣨�����ʳ�����������ߣ�
- ʵ����Ϸʤ��/ʧ���߼���ʳ��ľ�ʤ�����������߲���������ľ�ʧ�ܣ�
- ����HUD���棨������λ�á����������������Ͳ�����ʾ��

### 3. ��ͼϵͳ��map.py��
- `Map`�ࣺ��������״��ͼ�����ͱ߽磬ֻ��Ⱦ�����Ұ��Χ�ڵ�����
- `MinMap`�ࣺ���Ͻ�С��ͼ����ʾ���λ�ú�����ʳ��λ�ã�������������ʾ������ͼ

### 4. ʳ��ϵͳ��food.py��
- ���������10000x10000�ĵ�ͼ��Χ�ڣ�ȷ�������������������
- ʳ���ֵ�����`FOOD_MIN_VALUE`��`FOOD_MAX_VALUE`֮�䣩����ֵ��ͬ��ʾ��ɫ��ͬ
- ��������Ļ�ɼ���Χ�ڵ�ʳ��Ż�����

### 5. ������AI��hunter.py��
- ��������ϵͳ����Ϊ���ߣ��ܲ������ȶ��������������������Զ��ָ���
- ��Ҽ����׷�٣��� detection_range ��Χ�ڿɼ�⵽��ң�������Χ������λ��һ��ʱ��
- Ⱥ����Ϊ�����Ǹ��������ߵ�״̬���Ƿ��ڳ��/�ܲ�������������Ϊ����
- �����ƣ����ض����뷶Χ�ڣ�100-300���أ�����������ʱ���и�������ҳ��
- ·���Ż�����������ص㣬Ԥ������ƶ��켣

## ��Ϸ����
- ��������ǰ��������������
- ����Ҽ�����̣�����20����������ʱ����٣�
- ESC�����˳���Ϸ
- R������Ϸ���������¿�ʼ

## ��װ������
1. ��װ�����⣺
```bash
pip install pygame





# Explorer Game - README

## Game Introduction
This is an exploration survival game developed with Pygame. Players control an explorer to collect food for points while avoiding hunters. The game integrates a dynamic size system, energy management, and AI tracking mechanisms to deliver a strategic survival experience.

## Player System Details

### Core Attributes
- **Energy System**: Initial energy value is `PLAYER_INIT_ENERGY` with a maximum of 400. Energy naturally depletes over time and additionally consumes when moving or dashing.
- **Size Changes**: Dynamically changes based on energy level:
  - Energy = 0: Base size (1x base radius)
  - Energy = 200: 2x base radius
  - Energy = 400: 3x base radius
- **Speed Characteristics**: Inversely proportional to energy:
  - Energy = 0: 150% base speed
  - Energy = 200: 75% base speed
  - Energy = 400: 50% base speed

### Movement Mechanics
- **Movement Control**: Left mouse button to move forward; character automatically rotates toward mouse pointer.
- **Dash Function**: Triggered by right mouse button, consumes 20 energy points, and significantly increases movement speed temporarily (`PLAYER_DASH_SPEED_MULTIPLIER` times).
- **Energy Recovery**: Increase energy by collecting food; different value foods provide different energy points.

### Visual Presentation
- Light blue circular body that brightens when dashing
- Direction-aware eyes and mouth to enhance character expression
-ͷ�� energy bar showing current energy status with gradient (green��yellow��red)
- Translucent trail effect when dashing to enhance action feedback

## Project Structure
������ main.py # Program entry point, contains button classes and start screen
������ game.py # Main game logic, includes game loop and core mechanisms
������ player.py # Player class, handles movement, rotation, energy and rendering
������ map.py # Map and minimap related classes and drawing logic
������ food.py # Food entity class
������ hunter.py # Hunter AI class
������ audio.py # Audio management system
������ audio/ # Audio resource directory
������ eat.mp3 # Food collection sound effect
������ lost.mp3 # Game over sound effect
������ run.mp3 # Dash sound effect
������ win.mp3 # Victory sound effect

## Core Module Explanations

### 1. Audio System (audio.py)
- **AudioManager Class**: Object pool pattern-based audio management system
  - Initialization: Automatically detects and initializes Pygame audio system, supports custom minimum/maximum instance counts
  - Sound loading: Automatically loads basic sound effects from `audio` directory (eat/lost/run/win), provides warnings for missing files
  - Volume control: Offers `set_volume()` and `get_volume()` methods, supports global volume adjustment (0.0-1.0 range)
  - Instance management:
    - Dynamically maintains sound effect instance pool, automatically recycles completed instances
    - Supports simultaneous playback of multiple identical sounds (not exceeding maximum instance limit)
    - Automatically cleans up available instances exceeding minimum retention count for optimal resource usage
  - Playback control: `play_sound()` for playing specific sounds, `stop_sound()` to stop all instances of a sound, `clear_all()` to stop all sounds

### 2. Game Core (game.py)
- Manages main game loop, state updates and screen rendering
- Handles collision detection (player with food, player with hunters)
- Implements game win/lose logic (victory when all food is collected, defeat when caught by hunters or energy depleted)
- Renders HUD interface (score, position, nearby hunter count and operation hints)

### 3. Map System (map.py)
- `Map` class: Draws grid-based map background and boundaries, only renders area within player's field of view
- `MinMap` class: Top-right minimap showing player position and all food locations, displaying entire map proportionally

### 4. Food System (food.py)
- Spawns randomly within 10000x10000 map area, ensuring no spawns on player
- Food values random (between `FOOD_MIN_VALUE` and `FOOD_MAX_VALUE`), different values display different colors
- Only renders food within screen visibility range for performance optimization

### 5. Hunter AI (hunter.py)
- Stamina-based behavior decisions (running, charging consume stamina which automatically recovers)
- Player detection and tracking: Can detect players within detection_range, remembers position for a period after out of range
- Swarm behavior: Considers nearby hunters' states (charging/running) to adjust own behavior probability
- Charge mechanism: Has probability to charge at player within specific distance range (100-300 pixels) when stamina is sufficient
- Path optimization: Calculates interception points and predicts player movement trajectory

## Game Controls
- Left mouse button: Move forward (consumes energy)
- Right mouse button: Dash (consumes 20 energy points, temporarily accelerates)
- ESC key: Exit game
- R key: Restart after game over

## Installation and Running
1. Install dependencies:
```bash
pip install pygame