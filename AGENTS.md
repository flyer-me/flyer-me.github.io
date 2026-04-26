# 项目速览与 AI 助手指南

本文件为 AI 助手提供针对本仓库的可执行建议与约定要点。
目标是让 AI 能够快速完成常见任务（本地预览、构建校验、创建文章、维护元数据等）。

## 项目说明

站点为 Jekyll + Chirpy；GitHub Pages托管，通常不需要本地运行或发布步骤。
仓库保留工具脚本（如 `tools/*.sh`）用于开发，位于 `exclude` 列表里，不属于发布内容，不假定执行。

## 关键约定

- 不需更改 `_config.yml` 的 `permalink` 与 `defaults` 结构，这会影响现有文章链接。

- ## 编辑与新增文章的具体模式（示例）
- 可在 `_posts/` 中查看文章理解命名约定和正确 front-matter
- 图片在 `assets/img/posts/<YYYY-MM-DD-标题>/` 。
- 大型代码在 `_posts/code/` 。
- 文章使用相对路径引用资源

## AI 完成任务示例（带上下文）

- 创建文章：在 `_posts/` 中创建带有正确 front-matter 的文件，图片放入 `assets/img/posts/<slug>/`。
- 校验：若需要对生成的静态站点内容运行校验，请参考 `tools/test.sh`（仅供维护者/CI 使用），不要在自动 agent 的默认行为中运行该脚本。

## 提示语模板

- "为新文章生成 front-matter，标题为 'X'，类别 'Y'，标签 'A,B'，并把配图放到 `assets/img/posts/<slug>/`。请返回完整文件内容。"
- "检查 `_posts/2024-08-27-RPA实施：代码到低代码的实践.md` 的 front-matter，补全缺失的 `description`、`tags`，并建议图片路径。"
