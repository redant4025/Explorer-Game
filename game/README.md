# 探索者游戏 - README

## 游戏简介
这是一款基于Pygame开发的探索类生存游戏，玩家将控制探索者在地图中收集食物获取分数，同时需躲避狩猎者的追捕。游戏融合了动态体型系统、能量管理和AI追踪机制，带来富有策略性的生存体验。

## 玩家系统详解

### 核心属性
- **能量系统**：初始能量值为`PLAYER_INIT_ENERGY`，最大能量值为400，能量会随时间自然消耗，也会因移动和冲刺额外消耗
- **体型变化**：根据能量值动态改变大小
  - 能量=0时：基础体型（1倍基础半径）
  - 能量=200时：2倍基础半径
  - 能量=400时：3倍基础半径
- **速度特性**：与能量成反比关系
  - 能量=0时：150%基础速度
  - 能量=200时：75%基础速度
  - 能量=400时：50%基础速度

### 动作机制
- **移动控制**：通过鼠标左键控制前进，角色会自动朝向鼠标指针方向旋转
- **冲刺功能**：鼠标右键触发，消耗20点能量，短时间内大幅提升移动速度（`PLAYER_DASH_SPEED_MULTIPLIER`倍）
- **能量恢复**：通过收集食物增加能量，不同价值的食物提供不同能量值

### 视觉表现
- 浅蓝色圆形身体，冲刺时颜色变亮
- 随旋转方向变化的眼睛和嘴巴，增强角色表现力
- 头顶能量条直观显示当前能量状态（绿色→黄色→红色渐变）
- 冲刺时会留下半透明轨迹，提升动作反馈

## 项目结构
├── main.py # 程序入口，包含按钮类和开始界面
├── game.py # 游戏主逻辑，包含游戏循环和核心机制
├── player.py # 玩家类，处理移动、旋转、能量和绘制
├── map.py # 地图和小地图相关类与绘制逻辑
├── food.py # 食物实体类
├── hunter.py # 狩猎者 AI 类
├── audio.py # 音频管理系统
└── audio/ # 音频资源目录
├── eat.mp3 # 吃食物音效
├── lost.mp3 # 游戏失败音效
├── run.mp3 # 冲刺音效
└── win.mp3 # 游戏胜利音效

## 核心模块说明

### 1. 音频系统（audio.py）
- **AudioManager类**：基于对象池模式的音频管理系统
  - 初始化：自动检测并初始化Pygame音频系统，支持自定义最小/最大实例数
  - 音效加载：自动加载`audio`目录下的基础音效（eat/lost/run/win），缺失文件时给出警告
  - 音量控制：提供`set_volume()`和`get_volume()`方法，支持全局音量调节（0.0-1.0范围）
  - 实例管理：
    - 动态维护音效实例池，自动回收已完成播放的实例
    - 支持同时播放多个相同音效（不超过最大实例数限制）
    - 自动清理超出最小保留数的可用实例，优化资源占用
  - 播放控制：`play_sound()`播放指定音效，`stop_sound()`停止特定音效所有实例，`clear_all()`停止所有音效

### 2. 游戏核心（game.py）
- 管理游戏主循环、状态更新和画面渲染
- 处理碰撞检测（玩家与食物、玩家与狩猎者）
- 实现游戏胜利/失败逻辑（食物耗尽胜利、被狩猎者捕获或能量耗尽失败）
- 绘制HUD界面（分数、位置、附近狩猎者数量和操作提示）

### 3. 地图系统（map.py）
- `Map`类：绘制网格状地图背景和边界，只渲染玩家视野范围内的区域
- `MinMap`类：右上角小地图，显示玩家位置和所有食物位置，按比例缩略显示整个地图

### 4. 食物系统（food.py）
- 随机生成在10000x10000的地图范围内，确保不会生成在玩家身上
- 食物价值随机（`FOOD_MIN_VALUE`到`FOOD_MAX_VALUE`之间），价值不同显示颜色不同
- 仅绘制屏幕可见范围内的食物，优化性能

### 5. 狩猎者AI（hunter.py）
- 基于体力系统的行为决策（跑步、冲锋等动作消耗体力，体力可自动恢复）
- 玩家检测与追踪：在 detection_range 范围内可检测到玩家，超出范围后会记忆位置一段时间
- 群体行为：考虑附近狩猎者的状态（是否在冲锋/跑步）调整自身行为概率
- 冲锋机制：在特定距离范围内（100-300像素）且体力充足时，有概率向玩家冲锋
- 路径优化：会计算拦截点，预测玩家移动轨迹

## 游戏操作
- 鼠标左键：前进（消耗能量）
- 鼠标右键：冲刺（消耗20点能量，短时间加速）
- ESC键：退出游戏
- R键：游戏结束后重新开始

## 安装与运行
1. 安装依赖库：
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
-头顶 energy bar showing current energy status with gradient (green→yellow→red)
- Translucent trail effect when dashing to enhance action feedback

## Project Structure
├── main.py # Program entry point, contains button classes and start screen
├── game.py # Main game logic, includes game loop and core mechanisms
├── player.py # Player class, handles movement, rotation, energy and rendering
├── map.py # Map and minimap related classes and drawing logic
├── food.py # Food entity class
├── hunter.py # Hunter AI class
├── audio.py # Audio management system
└── audio/ # Audio resource directory
├── eat.mp3 # Food collection sound effect
├── lost.mp3 # Game over sound effect
├── run.mp3 # Dash sound effect
└── win.mp3 # Victory sound effect

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