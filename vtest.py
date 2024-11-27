import os
import subprocess
import pandas as pd

# 测试程序的根目录
TEST_DIR = "/home/rez/workbench/riscv-vector-tests/out/v512x64machine/bin/stage2/"
# 模拟器路径
EMULATOR = "/home/rez/workbench/prtest/sail-riscv/c_emulator/riscv_sim_RV64"
# 结果 CSV 文件路径
OUTPUT_CSV = "all_test_results.csv"

# 获取测试目录中的所有测试文件
test_files = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]

# 结果列表
results = []

# 遍历并运行每个测试文件
for test_path in test_files:
    print(f"Running {test_path}...")

    # 运行测试并捕获输出
    try:
        result = subprocess.run([EMULATOR, test_path], capture_output=True, text=True, timeout=60)
        last_line = result.stdout.splitlines()[-1] if result.stdout else ""
    except subprocess.TimeoutExpired:
        last_line = "TIMEOUT"

    # 判断测试结果
    if "FAILURE" in last_line:
        status = "FAILED"
    elif "TIMEOUT" in last_line:
        status = "TIMEOUT"
    else:
        status = "SUCCEEDED"

    # 保存测试结果
    results.append({
        "Test File": test_path,
        "Last Line": last_line,
        "Status": status
    })

# 生成结果表格
df_new = pd.DataFrame(results)

# 保存新的结果为 CSV 文件
df_new.to_csv(OUTPUT_CSV, index=False)

# 打印表格
print(df_new)
