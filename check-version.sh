#!/bin/sh
# 校验 SKILL.md 版本号与 CHANGELOG.md 最新条目是否一致。
#
# 背景：本技能曾被多个会话并行修改，出现过两次版本记录脱节——
#   1) v0.4.3 被两条改动线同时占用；
#   2) SKILL.md 已升到 v0.4.5，CHANGELOG 仍停在 v0.4.4。
# 该脚本用于提交前自查，本身不改动任何文件。
#
# 手动运行：  ./check-version.sh
# 挂成提交钩子（只警告、不阻断）：
#   ln -sf ../../check-version.sh .git/hooks/pre-commit
#
# 退出码：0 = 一致或无法判定；1 = 版本号不一致。

# 注意：本文件所有变量引用都用 ${v} 花括号形式。
# 在 sh 下 `$v` 后面紧跟中文字符时，中文字节会被并进变量名（`$v。` 被当作
# 一个变量），导致取值失败并把乱码打进输出。花括号可避免。

cd "$(dirname "$0")" || exit 0

skill_v=$(sed -n 's/^# 小胰宝 Humanizer v\([0-9][0-9.]*\).*/\1/p' SKILL.md | head -1)
log_v=$(sed -n 's/^## v\([0-9][0-9.]*\).*/\1/p' CHANGELOG.md | head -1)

if [ -z "${skill_v}" ] || [ -z "${log_v}" ]; then
  echo "check-version: 未能解析版本号 (SKILL.md=${skill_v} / CHANGELOG.md=${log_v})，跳过。"
  exit 0
fi

if [ "${skill_v}" = "${log_v}" ]; then
  echo "check-version: OK - SKILL.md 与 CHANGELOG.md 均为 v${skill_v}"
  exit 0
fi

echo "check-version: 版本号不一致"
echo "  SKILL.md      v${skill_v}"
echo "  CHANGELOG.md  v${log_v} (最新条目)"
echo "  请在 CHANGELOG.md 顶部补记 v${skill_v}，或修正 SKILL.md 版本头。"
exit 1
