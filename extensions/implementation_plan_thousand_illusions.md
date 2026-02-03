# 千幻无情道 - 改造实施计划文档

## 1. 引言

本文档旨在规划如何在不破坏原有架构的前提下，通过 Git 分支管理和模块化设计，实现“千幻无情道”世界设定。
核心目标是将开放的修仙世界调整为“单玩家本体 + 多分身历练”模式，同时保留原有代码的通用性，确保未来可以灵活切换或合并功能。

## 2. Git 分支管理策略

为了保证代码库的稳定性和可维护性，我们将采用以下分支策略：

*   **`main` (稳定分支)**: 
    *   保持原有的“开放修仙世界”设定。
    *   所有的通用 Bug 修复、性能优化、底层架构重构（非业务相关）都应首先提交到此分支。
*   **`feat/thousand-illusions` (特性分支)**:
    *   基于 `main` 分支创建。
    *   包含“千幻无情道”特有的逻辑实现（如 `MainBody` 类、特殊的 `IncarnationMixin` 逻辑、神念共鸣机制）。
    *   定期从 `main` 分支合并更新，以保持底层同步。

### 工作流示例
1.  **初始化**: `git checkout -b feat/thousand-illusions main`
2.  **开发**: 在 `feat/thousand-illusions` 上提交特定功能的代码。
3.  **同步**: 每周或重要更新后，执行 `git merge main` 将主分支的通用修复同步过来。
4.  **通用修复**: 如果发现通用 Bug，先切回 `main` 修复，然后同步到特性分支。

---

## 3. 代码改造计划

### 3.1 目录结构与配置 (static & tools)

#### static/game_configs
*   **新增配置**: 在 `feat/thousand-illusions` 分支中，新增 `static/game_configs/thousand_illusions.json` 或扩展现有 CSV，用于定义：
    *   本体初始属性。
    *   分身初始性格模板池（对应七情六欲）。
    *   道之感悟的阈值配置。
*   **兼容性**: 尽量不修改原有的 `world_info.csv` 等基础配置，而是通过代码逻辑在加载时进行覆盖或增量读取。

#### static/locales
*   **Prompt 模板**: 在 `static/locales/zh-CN/templates/` 下新增 `incarnation_events.txt`，用于生成分身觉醒、合道、神念共鸣时的剧情描述。
*   **UI 文本**: 更新前端多语言文件，增加“神念共鸣”、“觉醒度”、“合道”等词条。

#### tools
*   **初始化脚本**: 编写或修改 `tools/init_world.py` (假设存在或新建)，增加一个 `--mode=thousand_illusions` 参数。
    *   当启用该参数时，生成一个高修为的“隐世本体”和若干“低修为分身”，而不是随机生成平等的 NPC。

### 3.2 核心逻辑改造 (src)

我们将采用 **Mixin 扩展 + 策略模式** 来最大限度地复用代码。

#### src/classes/avatar/core.py (Avatar 类)
*   **现状**: `Avatar` 继承自 `ActionMixin`, `InventoryMixin` 等。
*   **改造**: 
    *   修改 `IncarnationMixin` (在 `src/classes/avatar/incarnation.py` 或类似位置)。
    *   确保 `IncarnationMixin` 中的逻辑（如 `strategy` 字段）默认对普通 NPC 不生效或保持默认值，仅在标记为 `is_incarnation=True` 时激活特殊逻辑。

```python
# src/classes/avatar/incarnation.py

class IncarnationMixin:
    is_incarnation: bool = False
    main_body_id: str = None  # 指向本体 ID
    awakening_level: float = 0.0
    accumulated_karma: float = 0
    # 恢复 strategy 字段，并增加 autonomous 选项
    # 选项: "immersive" (沉浸), "slaughter" (杀戮), "survival" (苟道), "autonomous" (自主)
    strategy: str = "immersive" 
    
    def check_awakening(self, event):
        """检查是否触发觉醒逻辑"""
        if not self.is_incarnation:
            return
        # ... 特有逻辑 ...
```

#### src/classes/main_body.py (新增)
*   创建一个新的类 `MainBody`，用于管理全局的“道”之状态。它可能不是一个在地图上移动的实体，而是一个更高维度的管理对象，或者是地图上一个特殊的不可见 Avatar。
*   功能：
    *   维护 `dao_insights` (道之感悟)。
    *   处理 `absorb_incarnation` (合道) 逻辑。
    *   提供 `resonate` (神念共鸣) 接口。

#### src/sim/simulator.py (模拟循环)
*   **引入游戏模式概念**:
    ```python
    # src/config.py 或 simulator.py
    class GameMode(Enum):
        OPEN_WORLD = "open_world"
        THOUSAND_ILLUSIONS = "thousand_illusions"

    CURRENT_GAME_MODE = GameMode.OPEN_WORLD # 默认值，可通过环境变量或配置修改
    ```
*   **循环注入**:
    在 `run_month` 或类似的循环函数中，插入钩子 (Hook)：
    ```python
    def run_month(self):
        # ... 原有逻辑 ...
        
        # 模式特有逻辑
        if CURRENT_GAME_MODE == GameMode.THOUSAND_ILLUSIONS:
            self.process_incarnation_sync() # 处理本体与分身的同步/共鸣
    ```

#### src/llm/ (AI 决策)
*   修改 Prompt 构建逻辑。当 Avatar 是分身且处于非“沉浸”策略时，System Prompt 中需要注入额外的指令（例如：“你是一具分身，你的核心目标是...，目前策略是...”）。
*   利用 `strategy` 字段动态调整 Prompt。

---

## 4. 实施步骤清单

### 阶段一：基础架构准备
1.  [ ] 创建 git 分支 `feat/thousand-illusions`。
2.  [ ] 在 `src/config.py` 中定义 `GameMode` 枚举及全局配置开关。
3.  [ ] 定义 `MainBody` 数据结构 (Python Class)。

### 阶段二：分身机制实现
1.  [ ] 修改 `IncarnationMixin`：
    *   [ ] 恢复 `strategy` 字段，添加枚举值。
    *   [ ] 实现 `is_incarnation` 标识及初始化逻辑。
    *   [ ] 实现 `awakening_level` 及其增长逻辑（基于事件触发）。
2.  [ ] 调整 `src/llm/prompt_builder.py` (假设存在)，根据 `strategy` 注入不同指令。
3.  [ ] 在 `static/locales` 中添加分身相关文本模板。

### 阶段三：神念共鸣与合道
1.  [ ] 实现“神念共鸣”功能：
    *   [ ] 前端/API 增加触发接口。
    *   [ ] 后端实现：消耗本体资源 -> 临时接管分身决策 -> 生成特殊行动建议。
2.  [ ] 实现“合道”功能：
    *   [ ] 定义合道条件（如觉醒度 100% 或 死亡）。
    *   [ ] 实现属性回收逻辑 (`MainBody` 吸收 `Avatar` 的 `accumulated_karma`)。

### 阶段四：验证与测试
1.  [ ] 编写单元测试：测试 `IncarnationMixin` 的状态流转。
2.  [ ] 集成测试：模拟运行 10 年，检查分身是否按 `strategy` 偏好行动，且能正确触发觉醒。
3.  [ ] 验证“神念共鸣”是否能成功干预 LLM 的决策输出。

## 5. 风险控制

*   **脏数据风险**: 确保新旧存档的兼容性。建议 `feat/thousand-illusions` 使用独立的存档目录或数据库表前缀。
*   **逻辑耦合**: 严禁在 `Avatar` 的通用方法中直接硬编码 `if mode == thousand_illusions`，应尽量使用 Hook、Mixin 或事件监听模式。

