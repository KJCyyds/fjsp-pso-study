import numpy as np
import matplotlib.pyplot as plt
import random

# 1. 简单的 FJSP 问题定义
# 格式：jobs[工件ID][工序ID] = {机器ID: 加工时间}
jobs_data = [
    [(0, 3), (1, 2), (2, 2)], # Job 0: Op0(M0:3s), Op1(M1:2s), Op2(M2:2s)
    [(0, 2), (2, 4), (1, 1)], # Job 1: Op0(M0:2s), Op1(M2:4s), Op2(M1:1s)
    [(1, 4), (0, 3), (2, 2)]  # Job 2: Op0(M1:4s), Op1(M0:3s), Op2(M2:2s)
]

num_jobs = len(jobs_data)
num_ops = len(jobs_data[0])
num_machines = 3

# 2. PSO 算法简易版
class Particle:
    def __init__(self):
        # 简化编码：每个工件的机器选择和顺序
        self.position = [random.randint(0, num_machines-1) for _ in range(num_jobs * num_ops)]
        self.best_position = list(self.position)
        self.fitness = float('inf')
        self.best_fitness = float('inf')

def calculate_makespan(position):
    machine_free_time = np.zeros(num_machines)
    job_last_op_time = np.zeros(num_jobs)
    schedule = []

    idx = 0
    for j in range(num_jobs):
        for o in range(num_ops):
            m_idx, p_time = jobs_data[j][o]
            start_time = max(machine_free_time[m_idx], job_last_op_time[j])
            end_time = start_time + p_time
            
            schedule.append((j, m_idx, start_time, end_time))
            machine_free_time[m_idx] = end_time
            job_last_op_time[j] = end_time
    return max(machine_free_time), schedule

# 3. 运行优化
particles = [Particle() for _ in range(20)]
best_global_fitness = float('inf')
best_schedule = []

for _ in range(100): # 迭代100次
    for p in particles:
        makespan, schedule = calculate_makespan(p.position)
        if makespan < p.best_fitness:
            p.best_fitness = makespan
            p.best_position = list(p.position)
        if makespan < best_global_fitness:
            best_global_fitness = makespan
            best_schedule = schedule

# 4. 绘制甘特图
def plot_gantt(schedule):
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['red', 'blue', 'green']
    for i, (job_id, m_idx, start, end) in enumerate(schedule):
        ax.barh(m_idx, end - start, left=start, color=colors[job_id], edgecolor='black', alpha=0.8)
        ax.text(start + (end-start)/2, m_idx, f'J{job_id}', va='center', ha='center', color='white')

    ax.set_xlabel('Time')
    ax.set_ylabel('Machine')
    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f'M{i}' for i in range(num_machines)])
    plt.title(f'FJSP Gantt Chart (PSO) - Optimal Makespan: {best_global_fitness}')
    plt.show()

print(f"最优化完工时间: {best_global_fitness}")
plot_gantt(best_schedule)