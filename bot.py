import requests
from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    player_id = request.form['player_id']
    player_info_url = f"https://api.truckersmp.com/v2/player/{player_id}"
    response = requests.get(player_info_url)
    player_info = response.json()

    # 解析玩家信息
    if not player_info["error"]:
        player_data = player_info["response"]
        player_id = player_data["id"]
        nickname = player_data["name"]
        join_date = player_data["joinDate"]
        steam_id = player_data["steamID"]
        group_name = player_data["groupName"]
        group_id = player_data["groupID"]
        banned = player_data["banned"]
        banned_until = player_data["bannedUntil"]
        bans_count = player_data["bansCount"]
        permissions = player_data["permissions"]
        vtc_history = player_data["vtcHistory"]

        # 计算加入天数
        join_datetime = datetime.strptime(join_date, "%Y-%m-%d %H:%M:%S")
        current_datetime = datetime.now()
        join_days = (current_datetime - join_datetime).days

        # 构建回复消息的格式
        reply_message = f"TMPID: {player_id}\n"
        reply_message += f"昵称: {nickname}\n"
        reply_message += f"加入时间: {join_date}\n"
        reply_message += f"加入天数: {join_days}天\n"
        reply_message += f"SteamID: {steam_id}\n"
        reply_message += f"联机用户组: {group_name}\n"
        reply_message += f"管理员: {'是' if permissions['isGameAdmin'] else '不是'}\n"
        reply_message += f"工作人员: {'是' if permissions['isStaff'] else '不是'}\n"
        reply_message += f"高层管理: {'是' if permissions['isManagement'] else '不是'}\n"

        if vtc_history:
            vtc = vtc_history[-1]
            reply_message += f"VTC: {vtc['name']}\n"
            reply_message += f"VTC ID: {vtc['id']}\n"
            reply_message += f"玩家加入过{len(vtc_history)}个vtc\n"
        else:
            reply_message += "VTC: 无\n"
            reply_message += "VTC ID: 无\n"
            reply_message += "玩家加入过0个vtc\n"

        reply_message += f"当前封禁: {'没有封禁' if not banned else '解封时间：' + banned_until}\n"
        reply_message += f"当前封禁次数: {bans_count}次\n"

    else:
        reply_message = "查询玩家信息失败"

    return render_template('index.html', result=reply_message)

if __name__ == '__main__':
    app.run(debug=True)
