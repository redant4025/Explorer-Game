import pygame
import os
from pygame import mixer

class AudioManager:
    def __init__(self, min_instances=2, max_instances=8):
        # 确保音频系统已初始化
        if not mixer.get_init():
            mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
        # 音效对象池：{音效名称: [可用实例列表, 正在使用实例列表]}
        self.sound_pools = {}
        self.sound_files = {}  # 存储音效文件路径
        self.min_instances = min_instances  # 最小保留实例数
        self.max_instances = max_instances  # 最大允许实例数
        self.audio_dir = "audio"    # 音频文件目录
        self.current_volume = 0.5   # 当前音量
        self.load_sounds()
        
    def load_sounds(self):
        """加载基础音效并初始化最小实例池"""
        try:
            # 确保音频目录存在
            if not os.path.exists(self.audio_dir):
                os.makedirs(self.audio_dir)
                print(f"创建音频目录: {self.audio_dir}")
            
            # 音效文件映射
            sound_files = {
                'eat': 'eat.mp3',
                'lost': 'lost.mp3',
                'run': 'run.mp3',
                'win': 'win.mp3',
            }
            
            for name, filename in sound_files.items():
                file_path = os.path.join(self.audio_dir, filename)
                
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    print(f"警告: 音效文件 {file_path} 不存在，跳过加载")
                    continue
                
                # 存储文件路径
                self.sound_files[name] = file_path
                
                # 初始化最小数量的实例
                pool = []
                for _ in range(self.min_instances):
                    try:
                        sound_instance = mixer.Sound(file_path)
                        sound_instance.set_volume(self.current_volume)
                        pool.append(sound_instance)
                    except pygame.error as e:
                        print(f"创建音效实例失败 {filename}: {e}")
                
                # 存储对象池：[可用实例, 正在使用实例]
                self.sound_pools[name] = [pool, []]
            
        except Exception as e:
            print(f"音效加载过程出错: {e}")
    
    def set_volume(self, volume):
        """设置所有音效的音量 (0.0-1.0)"""
        self.current_volume = max(0.0, min(1.0, volume))
        # 遍历所有对象池中的所有实例设置音量
        for available, in_use in self.sound_pools.values():
            for sound in available + in_use:
                sound.set_volume(self.current_volume)
    
    def get_volume(self):
        """获取当前音量"""
        return self.current_volume
    
    def play_sound(self, sound_name):
        """播放音效，动态管理实例"""
        if sound_name not in self.sound_pools:
            print(f"警告: 未找到音效 {sound_name}")
            return
        
        available, in_use = self.sound_pools[sound_name]
        
        # 清理已完成播放的实例，放回可用池
        self._cleanup_finished(sound_name)
        
        # 如果有可用实例，直接使用
        if available:
            sound = available.pop()
            sound.play()
            in_use.append(sound)
            return
        
        # 没有可用实例时，检查是否可以创建新实例
        total_instances = len(available) + len(in_use)
        if total_instances < self.max_instances:
            try:
                # 创建新实例
                new_sound = mixer.Sound(self.sound_files[sound_name])
                new_sound.set_volume(self.current_volume)
                new_sound.play()
                in_use.append(new_sound)
            except Exception as e:
                print(f"创建新音效实例失败: {e}")
        else:
            # 达到最大实例数，无法创建新实例
            print(f"警告: {sound_name} 已达到最大实例数 {self.max_instances}")
    
    def _cleanup_finished(self, sound_name):
        """将已完成播放的音效实例放回可用池"""
        available, in_use = self.sound_pools[sound_name]
        
        # 过滤掉已完成的音效
        remaining = []
        for sound in in_use:
            if sound.get_num_channels() == 0:
                available.append(sound)
            else:
                remaining.append(sound)
        
        # 更新正在使用的列表
        self.sound_pools[sound_name][1] = remaining
        
        # 清理超出最小保留数的可用实例（可选优化）
        self._prune_excess_instances(sound_name)
    
    def _prune_excess_instances(self, sound_name):
        """当可用实例超过最小保留数时，移除多余实例释放资源"""
        available, in_use = self.sound_pools[sound_name]
        if len(available) > self.min_instances:
            # 只保留最小数量的可用实例
            excess = len(available) - self.min_instances
            del available[:excess]
            print(f"清理 {sound_name} 的 {excess} 个多余实例")
    
    def stop_sound(self, sound_name):
        """停止指定音效的所有实例"""
        if sound_name in self.sound_pools:
            available, in_use = self.sound_pools[sound_name]
            for sound in available + in_use:
                sound.stop()
            # 将所有实例移回可用池
            self.sound_pools[sound_name] = [available + in_use, []]
            # 清理多余实例
            self._prune_excess_instances(sound_name)
    
    def clear_all(self):
        """停止所有音效并重置对象池"""
        for name in list(self.sound_pools.keys()):
            self.stop_sound(name)
    
    def quit(self):
        """清理并退出音频系统"""
        self.clear_all()
        mixer.quit()



audio_manager = AudioManager()
