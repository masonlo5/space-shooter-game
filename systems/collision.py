######################碰撞檢測系統######################

def check_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    """
    檢查兩個矩形物件是否碰撞\n
    \n
    使用 AABB (Axis-Aligned Bounding Box) 碰撞檢測算法\n
    \n
    參數:\n
    obj1_x, obj1_y, obj1_width, obj1_height (int): 物件1的位置和尺寸\n
    obj2_x, obj2_y, obj2_width, obj2_height (int): 物件2的位置和尺寸\n
    \n
    回傳:\n
    bool: 如果兩物件碰撞返回 True，否則返回 False\n
    """
    # 檢查兩個矩形是否有重疊
    return (obj1_x < obj2_x + obj2_width and
            obj1_x + obj1_width > obj2_x and
            obj1_y < obj2_y + obj2_height and
            obj1_y + obj1_height > obj2_y)