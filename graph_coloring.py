!pip install networkx matplotlib

import networkx as nx
import matplotlib.pyplot as plt

# تابع برای رنگ‌آمیزی گراف با الگوریتم حریصانه
def graph_coloring(adj_matrix, vertices, num_colors):
    # آرایه‌ای برای ذخیره رنگ هر رأس
    colors = [-1] * len(vertices)  # -1 یعنی هنوز رنگ نشده
    available_colors = list(range(num_colors))  # رنگ‌های موجود
    
    # اولین رأس را با رنگ 0 رنگ می‌کنیم
    colors[0] = 0
    
    # برای هر رأس دیگر
    for u in range(1, len(vertices)):
        # بررسی رنگ‌های رئوس مجاور
        used_colors = set()
        for v in range(len(vertices)):
            if adj_matrix[u][v] == 1 and colors[v] != -1:
                used_colors.add(colors[v])
        
        # اولین رنگ موجود که در رئوس مجاور استفاده نشده
        for color in available_colors:
            if color not in used_colors:
                colors[u] = color
                break
    
    # بررسی تعداد رنگ‌های استفاده‌شده
    used_colors = set(colors)
    min_colors = len(used_colors)
    
    return colors, min_colors

# تابع برای چاپ گراف با رنگ‌ها (خروجی متنی)
def print_colored_graph(vertices, edges, colors):
    print("\nگراف رنگ‌آمیزی‌شده:")
    for i, vertex in enumerate(vertices):
        print(f"رأس {vertex}: رنگ {colors[i]}")
    print("\nیال‌ها:")
    for edge in edges:
        print(f"{edge[0]} -- {edge[1]}")

# تابع برای رسم گراف با رنگ‌ها (خروجی گرافیکی)
def draw_colored_graph(vertices, edges, colors):
    # ایجاد گراف
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    
    # نگاشت رنگ‌ها به رئوس
    color_map = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']  # رنگ‌های قابل نمایش
    node_colors = [color_map[colors[i] % len(color_map)] for i in range(len(vertices))]
    
    # رسم گراف
    pos = nx.spring_layout(G)  # چیدمان رئوس
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=12, font_color='white')
    plt.title("گراف رنگ‌آمیزی‌شده")
    plt.show()

# تابع اصلی
def main():
    # دریافت تعداد رئوس
    n = int(input("تعداد رئوس را وارد کنید: "))
    vertices = []
    print("نام رئوس را وارد کنید (مثلاً a b c):")
    vertices = input().split()
    
    # دریافت تعداد یال‌ها
    m = int(input("تعداد یال‌ها را وارد کنید: "))
    edges = []
    print("یال‌ها را وارد کنید (مثلاً a b):")
    for i in range(m):
        u, v = input().split()
        edges.append((u, v))
    
    # دریافت تعداد رنگ‌های مجاز
    num_colors = int(input("تعداد رنگ‌های مجاز را وارد کنید: "))
    
    # ساخت ماتریس همسایگی
    adj_matrix = [[0] * n for _ in range(n)]
    vertex_index = {v: i for i, v in enumerate(vertices)}  # نگاشت نام رأس به اندیس
    
    for u, v in edges:
        i, j = vertex_index[u], vertex_index[v]
        adj_matrix[i][j] = 1
        adj_matrix[j][i] = 1  # گراف بدون جهت
    
    # چاپ ماتریس همسایگی
    print("\nماتریس همسایگی:")
    print("  ", end="")
    for v in vertices:
        print(v, end=" ")
    print()
    for i, row in enumerate(adj_matrix):
        print(vertices[i], end=" ")
        for val in row:
            print(val, end=" ")
        print()
    
    # رنگ‌آمیزی گراف
    colors, min_colors = graph_coloring(adj_matrix, vertices, num_colors)
    
    # چاپ نتایج
    print(f"\nحداقل تعداد رنگ‌های مورد نیاز: {min_colors}")
    print_colored_graph(vertices, edges, colors)
    
    # رسم گراف رنگ‌آمیزی‌شده
    draw_colored_graph(vertices, edges, colors)

# اجرای برنامه
if name == "__main__":
    main()