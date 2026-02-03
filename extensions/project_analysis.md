# 修仙世界模拟器 (Cultivation World Simulator) 项目设计分析

## 1. 项目概述

**修仙世界模拟器** 是一个 AI 驱动的开放世界修仙模拟引擎。不同于传统 RPG，本项目让玩家扮演 **“天道” (上帝)**，在规则与 AI 共同编织的开放世界中，观察众生百态，见证门派兴衰与天骄崛起。

核心技术栈：
- **后端**: Python 3.10+ (FastAPI)
- **前端**: Vue 3, TypeScript, Vite, PixiJS
- **并发模型**: AsyncIO (用于高并发 LLM 请求和 I/O 操作)
- **智能核心**: LLM Integration (OpenAI 兼容 / 本地 Ollama)
- **数据存储**: SQLite (事件持久化), JSON/CSV (静态配置)
- **部署**: Docker Compose

## 2. 核心设计哲学

项目致力于创造一个“真正活着的、有沉浸感的仙侠世界”，其设计哲学包含以下支柱：

### 2.1 “天道”视角 (God Mode)
玩家不直接控制特定角色，而是作为观察者和规则制定者。系统模拟了一个自运行的社会生态，玩家可以静观沧海桑田，也可以通过降下天劫、魔改心灵等方式微妙干预世界进程。

### 2.2 全员 AI 驱动 (Fully AI-Driven)
每个 NPC 都是独立的智能体，拥有：
-   **独立性格与记忆**: 基于 Persona 和 Memory 系统。
-   **动态人际关系**: 会结党营私，会有爱恨情仇。
-   **自主决策**: 根据当前局势和长短期目标 (Objectives) 做出行动判断。

### 2.3 规则即基石 (Rules as Bedrock)
为了防止 AI 产生幻觉或逻辑崩坏，世界运行在严谨的数值体系之上：
-   **修仙体系**: 灵根、境界、寿元、功法严格数值化。
-   **约束机制**: AI 的想象力被限制在合理的修仙逻辑框架内，确保世界真实可信。

### 2.4 涌现式剧情 (Emergent Storytelling)
系统没有预设剧本。宗门大战、正魔之争、天骄陨落等宏大叙事，皆由无数微小的个体因果逻辑自主推演而成。

## 3. 核心架构 (Core Architecture)

项目采用经典的 **Simulation Loop (模拟循环)** 架构，以“月”为基本时间单位 (`MonthStamp`) 推进世界发展。

### 3.1 模拟循环 (Simulator Loop)
位于 `src/sim/simulator.py`，主要流程如下：
1.  **感知阶段 (Perception)**: 更新所有角色的认知（如 `known_regions`），处理自动交互（如自动占据无主洞府）。
2.  **决策阶段 (Decision)**: 筛选当前空闲或需要新计划的角色，并发调用 AI (`LLMAI`) 生成行动计划。
3.  **执行阶段 (Execution)**: 推进所有角色的动作进度，处理动作完成后的结算。
4.  **世界事件结算**: 处理天地灵机 (Celestial Phenomena)、运气检测 (Fortune/Misfortune)、寿命结算等全局逻辑。

### 3.2 实体组件系统 (Entity System)
`Avatar` 类 (`src/classes/avatar/core.py`) 采用了 **Mixin 模式** 来避免“上帝类”过于臃肿：
-   `ActionMixin`: 处理动作队列、执行逻辑。
-   `InventoryMixin`: 处理背包、物品交互。
-   `EffectsMixin`: 处理 Buff/Debuff 状态。
-   `AvatarSaveMixin` / `AvatarLoadMixin`: 处理序列化与持久化。

## 4. 关键功能系统

### 4.1 动作系统与隔离策略 (Action System)
动作 (`Action`) 是角色与世界交互的基本单元。
-   **声明式隔离**: `Action` 基类引入了 `ALLOW_GATHERING` 和 `ALLOW_WORLD_EVENTS` 标志。例如 `Retreat` (闭关) 会将这些标志设为 `False`，从源头上屏蔽外部干扰，解决“闭关时乱跑”的问题。
-   **长时动作管理**: 通过 `@long_action` 装饰器，自动化处理跨月动作的进度管理。

### 4.2 宗门与组织 (Sects & Organizations)
不仅仅是标签，而是具有实体功能的组织：
-   **差异化风格**: 不同宗门有不同的功法、行事风格（如合欢宗双修、百兽宗御兽）。
-   **宗门动态**: 支持宗门大比、驻地管理等功能。

### 4.3 角色深度 (Avatar Depth)
-   **小剧场系统**: 战斗和对话会生成基于 LLM 的文本小剧场，增加代入感。
-   **状态追踪**: `AvatarMetrics` 记录修为、资源变化，生成角色年表。
-   **复杂属性**: 包含特质 (Traits)、江湖绰号 (Nicknames)、长短期目标。

### 4.4 事件系统 (Event System)
事件系统 (`src/classes/event_manager.py`) 经历了从纯内存到 SQLite 的重构。
-   **持久化**: 每个存档对应一个 `.db` 文件。
-   **高效查询**: 支持分页和多维度筛选（按角色、按关系对、按时间），保证长期运行性能。

## 5. 数据与配置

项目遵循 **代码与数据分离** 的原则：
-   **静态配置**: 游戏数值、物品定义、世界设定主要位于 CSV/JSON 文件中，通过 `src/run/data_loader.py` 加载。
-   **动态文本**: 提示词模版 (Prompt Templates) 独立存储，便于调整 AI 风格。

## 6. 国际化 (I18N)

项目实现了完整的国际化支持 (`src/i18n`)：
-   **方案**: 标准 GNU gettext (`.po` / `.mo` 文件)。
-   **范围**: 覆盖了静态配置文本和运行时生成的动态文本 (Dynamic Text)。

## 7. 扩展性设计：多世界观支持 (Extensibility for New Settings)

基于其模块化的架构，本项目支持在不破坏核心引擎的前提下，扩展全新的世界观设定（如“千幻无情道”或“现代都市恋爱”）。扩展遵循以下最佳实践：

### 7.1 分支管理策略 (Branch Strategy)
-   **Main 分支**: 维护通用的模拟引擎底层（事件系统、LLM 接口、基础 Mixin）。
-   **Feature 分支**: 每个独立的世界观设定（Setting）应在独立的 Feature 分支上开发（如 `feat/modern-romance`）。
-   **同步机制**: 定期将 Main 分支的底层优化合并至 Feature 分支，保持引擎能力同步。

### 7.2 代码层扩展 (Code Extension)
-   **GameMode 开关**: 在全局配置中引入 `GameMode` 枚举，用于在运行时区分当前激活的世界观。
-   **Mixin 扩展**: 针对特定世界观的角色逻辑，通过编写新的 Mixin 类（如 `ModernProfileMixin`, `IncarnationMixin`）并混入 `Avatar` 类来实现，避免修改 `core.py` 的通用逻辑。
-   **Hook 注入**: 在 `Simulator.run_month` 等核心循环中预留 Hook 点，允许不同模式注入特有的处理逻辑（如“现代模式”下的每日日程循环）。

### 7.3 数据层隔离 (Data Isolation)
-   **配置目录**: 推荐为新设定建立独立的配置目录（如 `static/game_configs/modern/`），通过加载器参数指定读取路径，从而替换原有的修仙界地图、物品和组织配置。
-   **Prompt 定制**: System Prompt 应支持根据 `GameMode` 动态切换，以适配不同的角色扮演语境（如将“道友”替换为“同事”）。

## 8. 总结

该项目通过将 LLM 的灵活性与传统 Simulation 的严谨性相结合，构建了一个高自由度的修仙沙盒。其技术架构（AsyncIO + Mixin + SQLite）能够支撑大量智能体的并发模拟，而“天道”视角的设计则为玩家提供了独特的观察体验。未来规划中的 MCP Agent 化和更丰富的世界法则（如转世、夺舍）将进一步增强其深度。
