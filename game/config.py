# config.py
import math

# 窗口和地图设置
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
MAP_WIDTH, MAP_HEIGHT = 5000, 10000
MIN_MAP_SIZE = 256

# 网格背景设置
GRID_SIZE = 100               # 网格单元的边长（像素）
GRID_COLOR = (40, 40, 40)     # 网格线颜色（深灰色）
GRID_LINE_WIDTH = 1           # 网格线的粗细（像素）

# 玩家参数（秒单位）
PLAYER_SPEED = 350             # 玩家移动基础速度（像素/秒）
PLAYER_ROTATION_SPEED = 300    # 玩家旋转速度（度/秒）
PLAYER_INIT_ENERGY = 100       # 初始能量值
PLAYER_MAX_ENERGY = 400        # 最大能量上限
PLAYER_ENERGY_LOSS_RATE = 1    # 随时间自然消耗的能量（每秒）
PLAYER_RADIUS = 20             # 玩家碰撞检测半径（像素）
PLAYER_FORWARD_ENERGY_COST = 6 # 向前移动时每秒消耗的能量
PLAYER_ENERGY_BAR_WIDTH = 40   # 头顶能量条的宽度（像素）
PLAYER_ENERGY_BAR_HEIGHT = 5   # 头顶能量条的高度（像素）
PLAYER_ENERGY_BAR_OFFSET = 30  # 能量条与玩家模型的垂直距离（像素）
# 冲刺相关配置
PLAYER_DASH_SPEED_MULTIPLIER = 3.0  # 冲刺时的速度倍率
PLAYER_DASH_ENERGY_COST = 15        # 每次冲刺消耗的能量
PLAYER_DASH_DURATION = 0.3          # 冲刺持续时间(秒)
# 速度与能量关系的系数
SPEED_ENERGY_BASE = 1.2        # 基础系数
SPEED_ENERGY_SCALE = 1.0       # 缩放系数


# 狩猎者参数（秒单位）
HUNTER_COUNT = 20                    # 狩猎者总数量
HUNTER_RADIUS = 25                   # 狩猎者碰撞检测半径（像素）
HUNTER_MAX_STAMINA = 100             # 最大耐力值
HUNTER_STAMINA_REGEN_RATE = 5        # 每秒恢复的耐力值
HUNTER_WALK_SPEED = 80               # 普通行走速度（像素/秒）
HUNTER_RUN_SPEED = 180               # 跑步速度（像素/秒）
HUNTER_CHARGE_SPEED = 500            # 冲锋时的爆发速度（像素/秒）
HUNTER_CHARGE_STAMINA_COST = 20      # 发起冲锋的基础耐力消耗
HUNTER_CHARGE_STAMINA_PER_PIXEL = 0.05  # 冲锋时每移动1像素额外消耗的耐力
HUNTER_RUN_STAMINA_COST_PER_SECOND = 5  # 跑步时每秒消耗的耐力
HUNTER_CHARGE_DISTANCE = 500         # 单次冲锋的最大距离（像素）
HUNTER_CHARGE_COOLDOWN = 2           # 冲锋后的冷却时间（秒）
HUNTER_NORMAL_ROTATION_SPEED = 100   # 普通状态下的旋转速度（度/秒）
HUNTER_RUN_ROTATION_SPEED = 110      # 跑步时的旋转速度（度/秒）
HUNTER_CHARGE_ROTATION_SPEED = 120   # 冲锋时的旋转速度（度/秒）
HUNTER_STOP_ROTATION_SPEED_RATIO = 0.5  # 耐力不足时的旋转速度比例
HUNTER_MIN_CHARGE_DISTANCE = 150     # 发起冲锋的最小距离（像素）
HUNTER_MAX_CHARGE_DISTANCE = 700     # 发起冲锋的最大距离（像素）
HUNTER_HIGH_CHANCE_RANGE_START = 200 # 高冲锋概率区间的起始距离（像素）
HUNTER_HIGH_CHANCE_RANGE_END = 500   # 高概率区间的结束距离（像素）
HUNTER_HIGH_CHARGE_CHANCE = 1.8      # 高概率区间内的冲锋触发概率（每秒）
HUNTER_LOW_CHARGE_CHANCE = 0.6       # 低概率区间内的冲锋触发概率（每秒）
HUNTER_STAMINA_THRESHOLD = 20        # 耐力低于此值时进入"停止状态"
HUNTER_RUN_STAMINA_THRESHOLD = 10    # 跑步所需的最低耐力（降低至10，允许更多跑步）
HUNTER_DETECTION_RANGE = 1200        # 狩猎者探测玩家的范围（像素）
HUNTER_WANDER_AREA = 3000            # 未发现玩家时的随机游走范围（像素）
HUNTER_WANDER_CHANGE_INTERVAL = (3, 8)  # 随机游走目标点的更换间隔范围（秒）
HUNTER_GROUP_BEHAVIOR_RADIUS = 800   # 狩猎者之间的群体行为范围
HUNTER_AVOID_COLLISION_RADIUS = 100  # 狩猎者之间避免碰撞的距离
HUNTER_CHARGE_TURN_RATIO = 0.7       # 冲锋时转向幅度比例（保留一定惯性）
#猎人会在距离目标 HUNTER_RUN_RANGE_MIN-HUNTER_RUN_RANGE_MAX 像素的范围内考虑跑步
HUNTER_RUN_RANGE_MIN = 200
HUNTER_RUN_RANGE_MAX = 800 

# 食物参数
FOOD_COUNT = 50                     # 地图上同时存在的食物总数
FOOD_RADIUS = 10                     # 食物碰撞检测半径（像素）
FOOD_MIN_VALUE = 10                  # 单个食物的最小能量值
FOOD_MAX_VALUE = 60                  # 单个食物的最大能量值

# 音频设置
BACKGROUND_MUSIC_PATH = "audio/VUICAARISWS.mid"  # 默认背景音乐路径
MUSIC_VOLUME = 0.2  # 背景音乐音量 (0.0-1.0)

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
ENERGY_BAR_BACKGROUND = (50, 50, 50)
BOUNDARY_COLOR = (100, 100, 100)  # 深灰色边界（RGB值）
CYAN = (0, 255, 255)    # 新增：跑步状态颜色（青色）
