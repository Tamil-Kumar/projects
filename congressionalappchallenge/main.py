import customtkinter as ctk
from PIL import Image
import json
import os
from datetime import datetime, timedelta
import traceback

USER_DB_FILE = "users.json"
BADGE_RULES = [
    {"id": "beginner", "emoji": "🎓", "name": "Beginner Badge", "condition": lambda u: "Lesson 1: Variables" in u.get("completed_lessons", [])},
    {"id": "intermediate", "emoji": "📘", "name": "Intermediate Badge", "condition": lambda u: "Lesson 1: For Loops" in u.get("completed_lessons", [])},
    {"id": "advanced", "emoji": "📗", "name": "Advanced Badge", "condition": lambda u: "Lesson 1: Functions" in u.get("completed_lessons", [])},
    {"id": "xp50", "emoji": "💪", "name": "XP 50 Badge", "condition": lambda u: u.get("xp", 0) >= 50},
    {"id": "xp100", "emoji": "🧠", "name": "XP 100 Badge", "condition": lambda u: u.get("xp", 0) >= 100},
    {"id": "xp200", "emoji": "⚡", "name": "XP 200 Badge", "condition": lambda u: u.get("xp", 0) >= 200},
    {"id": "xp300", "emoji": "🌟", "name": "XP 300 Badge", "condition": lambda u: u.get("xp", 0) >= 300},
    {"id": "streak5", "emoji": "🔥", "name": "Streak Master", "condition": lambda u: u.get("streak", 0) >= 5},
    {"id": "top_leader", "emoji": "👑", "name": "Top Learner (5 Days)", "condition": lambda u: u.get("top_days", 0) >= 5},
    {"id": "loops", "emoji": "🧪", "name": "Loop Learner", "condition": lambda u: any("loop" in title.lower() for title in u.get("completed_lessons", []))},
    {"id": "functions", "emoji": "🧮", "name": "Function Fan", "condition": lambda u: any("functions" in title.lower() for title in u.get("completed_lessons", []))},
    {"id": "string_star", "emoji": "💬", "name": "String Star", "condition": lambda u: any("string" in title.lower() or "strings" in title.lower() for title in u.get("completed_lessons", []))},
    {"id": "list_legend", "emoji": "📋", "name": "List Legend", "condition": lambda u: any("list" in title.lower() for title in u.get("completed_lessons", []))},
    {"id": "dict_master", "emoji": "📖", "name": "Dictionary Master", "condition": lambda u: "Lesson 4: Dictionaries" in u.get("completed_lessons", [])},
    {"id": "input_inquisitor", "emoji": "⌨️", "name": "Input Inquisitor", "condition": lambda u: "Lesson 5: Input" in u.get("completed_lessons", [])},
    {"id": "math_mage", "emoji": "➗", "name": "Math Mage", "condition": lambda u: "Lesson 6: Math Operations" in u.get("completed_lessons", [])},
    {"id": "file_reader", "emoji": "📂", "name": "File Reader", "condition": lambda u: "Lesson 10: Reading Files" in u.get("completed_lessons", [])},
    {"id": "master", "emoji": "🧙‍♂️", "name": "Master Coder", "condition": lambda u: u.get("skill_level") == "Master"},
]

def get_badges(user):
    return [rule["emoji"] for rule in BADGE_RULES if rule["condition"](user)]

def get_badge_info():
    return [(rule["emoji"], rule["name"]) for rule in BADGE_RULES]

def show_home():
    global home_frame
    home_frame = ctk.CTkFrame(app)
    home_frame.pack(fill="both", expand=True)

    # --- Topbar ---
    topbar = ctk.CTkFrame(home_frame, fg_color="transparent")
    topbar.pack(fill="x", pady=10, padx=20)

    ctk.CTkLabel(
        topbar, text="🐍 SkillScreen",
        font=("Helvetica", 28, "bold")
    ).pack(side="left", padx=10)

    if user_data["username"]:  # logged in
        ctk.CTkButton(
            topbar, text="👤 Profile", width=130, height=40,
            corner_radius=20, font=("Helvetica", 14, "bold"),
            command=lambda: [home_frame.pack_forget(), build_main_ui()]
        ).pack(side="right", padx=5)
    else:
        ctk.CTkButton(
            topbar, text="Login", width=110, height=40,
            corner_radius=20, font=("Helvetica", 14, "bold"),
            command=lambda: [home_frame.pack_forget(), switch_to_login()]
        ).pack(side="right", padx=5)
        ctk.CTkButton(
            topbar, text="Register", width=110, height=40,
            corner_radius=20, font=("Helvetica", 14, "bold"),
            fg_color="#3b82f6", hover_color="#2563eb",
            command=lambda: [home_frame.pack_forget(), switch_to_register()]
        ).pack(side="right", padx=5)

    # --- Hero Section ---
    hero = ctk.CTkFrame(home_frame, corner_radius=12, fg_color="#1e293b")
    hero.pack(fill="x", padx=30, pady=20)

    try:
        python_logo = ctk.CTkImage(
            light_image=Image.open("python_logo.png"),
            dark_image=Image.open("python_logo.png"),
            size=(80, 80)
        )
        ctk.CTkLabel(hero, image=python_logo, text="").pack(side="left", padx=20, pady=20)
    except Exception:
        pass

    text_frame = ctk.CTkFrame(hero, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True, pady=20)

    ctk.CTkLabel(
        text_frame, text="Master Python, Step by Step 🚀",
        font=("Helvetica", 28, "bold"), text_color="white", anchor="w"
    ).pack(anchor="w")

    ctk.CTkLabel(
        text_frame,
        text="Interactive lessons • XP rewards • Track your progress",
        font=("Helvetica", 16), text_color="#cbd5e1", anchor="w"
    ).pack(anchor="w", pady=(5, 0))

    if user_data["username"]:
        stats = ctk.CTkFrame(hero, corner_radius=10, fg_color="#334155")
        stats.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkLabel(stats, text=f"⭐ XP: {user_data.get('xp',0)}", font=("Helvetica", 14)).pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(stats, text=f"🔥 Streak: {user_data.get('streak',0)} days", font=("Helvetica", 14)).pack(side="left", padx=15)
        badge_line = " ".join(get_badges(user_data))
        if badge_line:
            ctk.CTkLabel(stats, text=f"🏅 Badges: {badge_line}", font=("Helvetica", 14)).pack(side="left", padx=15)

    # --- Tabview ---
    tabview = ctk.CTkTabview(home_frame, width=1000, height=600, corner_radius=12)
    tabview.pack(anchor="nw", padx=30, pady=20, fill="both", expand=True)

    try:
        tabview._segmented_button.configure(
            font=("Helvetica", 18, "bold"),
            fg_color="#334155",
            selected_color="#3b82f6",
            unselected_color="#475569"
        )
    except Exception:
        pass

    # Tabs
    tab1 = tabview.add("🎓 Why Learn Python?")
    tab2 = tabview.add("🚀 Features")
    tab3 = tabview.add("🌍 Who Uses Python?")
    tab4 = tabview.add("ℹ About")  # NEW TAB

    def add_content(parent, heading, highlights, paragraph):
        container = ctk.CTkFrame(parent, corner_radius=12, fg_color="#334155")
        container.pack(padx=40, pady=30, fill="both", expand=True)

        ctk.CTkLabel(
            container, text=heading,
            font=("Helvetica", 22, "bold"), text_color="white", anchor="w"
        ).pack(anchor="w", pady=(10, 15))

        for hl in highlights:
            ctk.CTkLabel(
                container, text=f"• {hl}",
                font=("Helvetica", 16), anchor="w", text_color="white"
            ).pack(anchor="w", padx=20, pady=2)

        ctk.CTkLabel(
            container, text=paragraph,
            font=("Helvetica", 15), justify="left",
            wraplength=800, text_color="white"
        ).pack(anchor="w", padx=20, pady=(15, 20))

    # --- Tab 1 ---
    add_content(
        tab1,
        "Why Learn Python?",
        ["Easy to read and write", "Perfect for beginners", "Lots of free learning resources", "Huge community support"],
        "Python is one of the fastest-growing languages. It powers AI, web development, data science, and automation."
    )

    # --- Tab 2 ---
    add_content(
        tab2,
        "Key Features of Python",
        ["Interpreted and beginner-friendly", "Supports OOP, Functional, and Procedural styles", "Over 350,000 libraries available", "Used in AI, web apps, automation, data science"],
        "Python adapts to many fields. From building websites with Django to analyzing data with Pandas, its versatility is unmatched."
    )

    # --- Tab 3 ---
    add_content(
        tab3,
        "Who Uses Python?",
        ["Google – search algorithms and AI", "Instagram – backend services", "Netflix – recommendation engine", "NASA – scientific computing", "Spotify – data analytics"],
        "Python is trusted by startups and tech giants alike."
    )

    # --- Tab 4 (About) ---
    add_content(
        tab4,
        "About Me",
        ["13 years old", "Goes to Middle North Middle School", "Has a pet dog named Ginger", "Plays piano and flute", "Coding in Python for 2 years", "Coding in general for over 4 years", "Learned HTML, CSS, JavaScript, C++, C#, C, and Python"],
        ""
    )

# Reusable home button
def add_home_button(frame, current_frame):
    topbar = ctk.CTkFrame(frame)
    topbar.pack(fill="x", pady=5, padx=10)
    ctk.CTkButton(topbar, text="🏠 Home", width=100, height=35,
                  command=lambda: [current_frame.pack_forget(), show_home()]).pack(side="right", padx=5)

def load_users():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = {}
    else:
        users = {}
    if "admin" not in users:
        users["admin"] = {
            "password": "root",
            "skill_level": "Admin",
            "xp": 0,
            "streak": 0,
            "last_login": None,
            "completed_lessons": [],
        }
        save_users(users)
    return users

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_current_date():
    return test_date_override or datetime.now().date()

user_data = {"username":"", "skill_level":"", "xp":0, "streak":0, "last_login":None, "completed_lessons": []}
test_date_override = None

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")
app.title("Learn Python")

login_frame = ctk.CTkFrame(app)
register_frame = ctk.CTkFrame(app)
main_frame = None

username_entry_login = password_entry_login = login_error_label = None
username_entry_register = password_entry_register = register_error_label = skill_level = None

def logout():
    global main_frame
    if main_frame:
        main_frame.destroy()

    user_data.update({
        "username": "", "skill_level": "",
        "xp": 0, "streak": 0, "last_login": None
    })

    if username_entry_login:
        username_entry_login.delete(0, "end")
    if password_entry_login:
        password_entry_login.delete(0, "end")

    if username_entry_register:
        username_entry_register.delete(0, "end")
    if password_entry_register:
        password_entry_register.delete(0, "end")
    if skill_level:
        skill_level.set("Beginner")

    switch_to_login()

def handle_login():
    users = load_users()
    u = username_entry_login.get().strip()
    p = password_entry_login.get().strip()
    if u in users and users[u]["password"] == p:
        user = users[u]
        user_data.update({
            "username":u,
            "subject":user.get("subject","General"),
            "skill_level":user.get("skill_level",""),
            "xp":user.get("xp",0),
            "streak":user.get("streak",0),
            "last_login":user.get("last_login")
        })
        user_data["completed_lessons"] = user.get("completed_lessons", [])
        login_error_label.configure(text="")
        login_frame.pack_forget()
        build_main_ui()
    else:
        login_error_label.configure(text="Invalid username or password")

def handle_register():
    users = load_users()
    u = username_entry_register.get().strip()
    p = password_entry_register.get().strip()
    subj = subject_var.get()
    s = skill_level_var.get()
    if not u or not p:
        register_error_label.configure(text="Please fill in all fields")
        return
    if u in users:
        register_error_label.configure(text="User already exists!")
        return
    users[u] = {"password":p,"subject":subj,"skill_level":s,"xp":0,"streak":0,"last_login":None}
    save_users(users)
    user_data.update({"username":u,"subject":subj,"skill_level":s,"xp":0,"streak":0,"last_login":None})
    register_error_label.configure(text="")
    register_frame.pack_forget()
    build_main_ui()

def switch_to_register():
    register_frame.pack(fill="both",expand=True)
    login_frame.pack_forget()
    login_error_label.configure(text="")
    register_error_label.configure(text="")

def switch_to_login():
    login_frame.pack(fill="both",expand=True)
    register_frame.pack_forget()
    login_error_label.configure(text="")
    register_error_label.configure(text="")

def setup_login_frame():
    global username_entry_login, password_entry_login, login_error_label
    ctk.CTkLabel(login_frame,text="🔐 Login",font=("Helvetica",24,"bold")).pack(pady=20)
    username_entry_login = ctk.CTkEntry(login_frame,placeholder_text="Username",width=250); username_entry_login.pack(pady=10)
    password_entry_login = ctk.CTkEntry(login_frame,placeholder_text="Password",show="*",width=250); password_entry_login.pack(pady=10)
    login_error_label = ctk.CTkLabel(login_frame,text="",text_color="red",font=("Helvetica",12)); login_error_label.pack(pady=(5,0))
    ctk.CTkButton(login_frame,text="Login",width=200,command=handle_login).pack(pady=15)
    ctk.CTkButton(login_frame,text="Register Instead",width=200,command=switch_to_register).pack()


def setup_register_frame():
    global username_entry_register, password_entry_register, register_error_label, subject_var, skill_level_var
    ctk.CTkLabel(register_frame,text="📝 Register",font=("Helvetica",24,"bold")).pack(pady=20)
    username_entry_register = ctk.CTkEntry(register_frame,placeholder_text="Username",width=250); username_entry_register.pack(pady=8)
    password_entry_register = ctk.CTkEntry(register_frame,placeholder_text="Password",show="*",width=250); password_entry_register.pack(pady=8)
    
    subject_var = ctk.StringVar(value="General")
    skill_level_var = ctk.StringVar(value="Beginner")

    def update_skill_levels(subject):
        skill_menu.configure(values=["Beginner","Intermediate","Advanced"])
        skill_level_var.set("Beginner")

    ctk.CTkLabel(register_frame, text="Select Subject:").pack(pady=(10,0))
    subject_menu = ctk.CTkOptionMenu(register_frame, values=["General","Math","Physics"], variable=subject_var, command=update_skill_levels)
    subject_menu.pack(pady=5)

    ctk.CTkLabel(register_frame, text="Select Skill Level:").pack(pady=(10,0))
    skill_menu = ctk.CTkOptionMenu(register_frame, values=["Beginner","Intermediate","Advanced"], variable=skill_level_var)
    skill_menu.pack(pady=5)

    register_error_label = ctk.CTkLabel(register_frame,text="",text_color="red",font=("Helvetica",12)); register_error_label.pack(pady=(5,0))
    ctk.CTkButton(register_frame,text="Register",width=200,command=handle_register).pack(pady=15)
    ctk.CTkButton(register_frame,text="Back to Login",width=200,command=switch_to_login).pack()


def build_main_ui():
    global main_frame
    users = load_users()
    imgs = [Image.open(f'images\\{name}_icon.png') for name in ["login_rewards","leaderboard","profile","learn"]]
    icons = [ctk.CTkImage(img,size=(24,24)) for img in imgs]
    login_img, leaderboard_img, profile_img, learn_img = icons

    if main_frame: main_frame.destroy()
    main_frame = ctk.CTkFrame(app); main_frame.pack(fill="both",expand=True)
    sidebar = ctk.CTkFrame(main_frame,width=180,corner_radius=0); sidebar.pack(side="left",fill="y")
    content_frame = ctk.CTkFrame(main_frame,corner_radius=10); content_frame.pack(side="right",fill="both",expand=True,padx=10,pady=10)

    def clear_content(): 
        for w in content_frame.winfo_children(): w.destroy()

    def show_profile():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="👤 Profile", font=("Helvetica",24,"bold")).pack(pady=(20,10))
        pf = ctk.CTkFrame(content_frame, corner_radius=10); pf.pack(pady=10,padx=30,fill="x")
        ctk.CTkLabel(pf, text="🧑", font=("Helvetica",50)).pack(pady=10)
        key_map = {
            "Username": "username",
            "Subject": "subject",
            "Skill Level": "skill_level",
            "XP": "xp",
            "Streak": "streak"
        }
        for k in key_map:
            v = user_data.get(key_map[k], "")
            if k=="Streak":
                v = f"{user_data.get('streak',0)} days"
            row = ctk.CTkFrame(pf); row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=f"{k}:", width=100, anchor="w", font=("Helvetica",13,"bold")).pack(side="left")
            ctk.CTkLabel(row, text=str(v), font=("Helvetica",13)).pack(side="left")

        # Subject changer
        ctk.CTkLabel(pf, text="Change Subject:", font=("Helvetica",13,"bold")).pack(pady=(10,0))
        subject_change_var = ctk.StringVar(value=user_data.get("subject", "General"))
        subject_menu = ctk.CTkOptionMenu(pf, values=["General","Math","Physics"], variable=subject_change_var)
        subject_menu.pack(pady=5)

        def save_subject_change():
            new_subject = subject_change_var.get()
            user_data["subject"] = new_subject
            user_data["skill_level"] = "Beginner"  # reset to beginner in new subject
            users_db = load_users()
            users_db[user_data["username"]]["subject"] = new_subject
            users_db[user_data["username"]]["skill_level"] = "Beginner"
            save_users(users_db)
            ctk.CTkLabel(pf, text=f"✅ Subject changed to {new_subject} (Beginner)", text_color="green").pack(pady=5)

        ctk.CTkButton(pf, text="Save Subject", command=save_subject_change).pack(pady=5)

        badge_line = " ".join(get_badges(user_data))
        ctk.CTkLabel(pf, text=f"🏅 Badges: {badge_line}", font=("Helvetica",14)).pack(pady=5)

    def show_leaderboard():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="🏆 Leaderboard", font=("Helvetica",22,"bold")).pack(pady=10)
        b = ctk.CTkFrame(content_frame); b.pack(fill="x",padx=30,pady=10)
        rankings = [(u,data) for u,data in load_users().items() if u!="admin"]
        rankings.sort(key=lambda x: x[1].get("xp",0), reverse=True)
        for idx,(u,data) in enumerate(rankings[:10],start=1):
            badges = get_badges(data)
            badge_str = " ".join(badges)
            ctk.CTkLabel(b,text=f"{idx}. {u} {badge_str} - {data.get('xp',0)} XP",font=("Helvetica",14)).pack(anchor="w",padx=10,pady=5)

    def show_badges():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="🎖️ All Badges", font=("Helvetica", 22, "bold")).pack(pady=10)
        for emoji, name in get_badge_info():
            owned = emoji in get_badges(user_data)
            color = "green" if owned else "gray"
            ctk.CTkLabel(content_frame, text=f"{emoji} {name}", text_color=color, font=("Helvetica", 16)).pack(anchor="w", padx=30, pady=3)

    def show_rewards():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="🎁 Daily Login Rewards", font=("Helvetica",24,"bold")).pack(pady=(20,10))
        rb = ctk.CTkFrame(content_frame,corner_radius=10); rb.pack(padx=40,pady=15,fill="x")
        ctk.CTkLabel(rb, text="+5 XP",font=("Helvetica",20,"bold"),text_color="white",fg_color="#3b82f6").pack(fill="x",pady=10)
        ctk.CTkLabel(rb, text=f"🔥 Streak: {user_data.get('streak',0)} days",font=("Helvetica",14)).pack(fill="x",pady=10)
        def can_claim():
            last = user_data.get("last_login")
            return not last or datetime.strptime(last,"%Y-%m-%d").date() < get_current_date()
        status = ctk.CTkLabel(content_frame, text="", font=("Helvetica",12)); status.pack(pady=5)
        btn = ctk.CTkButton(content_frame, text="Claim Reward", width=180,height=40); btn.pack(pady=10)
        def claim():
            if not can_claim():
                status.configure(text="Already claimed today."); btn.configure(state="disabled"); return
            today = get_current_date()
            last = user_data.get("last_login")
            if last and datetime.strptime(last,"%Y-%m-%d").date() == today - timedelta(days=1):
                user_data["streak"] += 1
            else:
                user_data["streak"] = 1
            user_data["xp"] += 5
            user_data["last_login"] = today.strftime("%Y-%m-%d")
            u = load_users()
            u[user_data["username"]].update({"xp":user_data["xp"], "streak":user_data["streak"], "last_login": user_data["last_login"]})
            save_users(u)
            status.configure(text="Claimed! +5 XP awarded."); btn.configure(state="disabled")
        if can_claim():
            status.configure(text="You can claim today."); btn.configure(command=claim,state="normal")
        else:
            status.configure(text="Already claimed today."); btn.configure(state="disabled")

    def show_learn():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="📘 Learn Python", font=("Helvetica",22,"bold")).pack(pady=10)

        try:
            with open("lessons.json", "r") as f:
                lessons_data = json.load(f)
        except Exception as e:
            ctk.CTkLabel(content_frame, text="Error loading lessons.", text_color="red").pack()
            return

        subj = user_data.get("subject", "General")
        level = user_data.get("skill_level", "Beginner")

        # --- Handle Master level ---
        if level == "Master":
            ctk.CTkLabel(
                content_frame,
                text="🎉 Congratulations! You've completed all lessons in this subject.",
                text_color="green", font=("Helvetica", 18, "bold"),
                wraplength=600, justify="center"
            ).pack(pady=40)
            ctk.CTkLabel(
                content_frame,
                text="You are now a Master in this subject.\nKeep practicing and exploring new projects!",
                font=("Helvetica", 14), wraplength=600, justify="center"
            ).pack(pady=20)

            # Restart button
            def restart_subject():
                users_db = load_users()
                username = user_data["username"]

                # Reset their skill level back to Beginner
                user_data["skill_level"] = "Beginner"
                users_db[username]["skill_level"] = "Beginner"

                # Clear completed lessons for this subject
                user_data["completed_lessons"] = []
                users_db[username]["completed_lessons"] = []

                save_users(users_db)

                # Refresh the Learn screen
                clear_content()
                show_learn()

            ctk.CTkButton(
                content_frame, text="🔄 Restart Subject",
                fg_color="#3b82f6", hover_color="#2563eb",
                command=restart_subject, width=200, height=40
            ).pack(pady=20)

            return

        # --- Normal lesson flow ---
        lessons = lessons_data.get(subj, {}).get(level, [])
        if not lessons:
            ctk.CTkLabel(content_frame, text="No lessons found for your level.", text_color="red").pack()
            return

        current_lesson_idx = [0]

        users_db = load_users()
        user_rec = users_db.get(user_data["username"], {})
        completed = set(user_rec.get("completed_lessons", []))

        # --- Scrollable Frame for Lessons ---
        scrollable = ctk.CTkScrollableFrame(content_frame, corner_radius=10)
        scrollable.pack(padx=30, pady=10, fill="both", expand=True)

        lesson_frame = ctk.CTkFrame(scrollable)
        lesson_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def load_lesson(idx):
            for w in lesson_frame.winfo_children():
                w.destroy()

            lesson = lessons[idx]
            title = lesson["title"]
            content = lesson["content"]
            xp_reward = lesson.get("xp_reward", 0)

            ctk.CTkLabel(lesson_frame, text=title, font=("Helvetica",18,"bold")).pack(anchor="w", pady=(0,10))
            ctk.CTkLabel(lesson_frame, text=content, wraplength=520, justify="left").pack(anchor="w", pady=(0,10))
            ctk.CTkLabel(lesson_frame, text="Type your code below and run it:", font=("Helvetica",14,"bold")).pack(anchor="w")

            code_text = ctk.CTkTextbox(lesson_frame, width=600, height=150)
            code_text.pack(pady=(5,10))

            output_label = ctk.CTkLabel(
                lesson_frame, text="", font=("Courier", 12), text_color="white",
                fg_color="#333333", corner_radius=5, height=100, width=600,
                wraplength=580, justify="left"
            )
            output_label.pack(pady=(5,10))

            def run_user_code():
                code = code_text.get("1.0", "end").strip()
                try:
                    import io, sys
                    buffer = io.StringIO()
                    sys_stdout = sys.stdout
                    sys.stdout = buffer

                    exec(code, {})

                    sys.stdout = sys_stdout
                    output = buffer.getvalue()
                    output_label.configure(text=output if output else "(No output)")
                except Exception as e:
                    sys.stdout = sys_stdout
                    output_label.configure(text=traceback.format_exc())

            ctk.CTkButton(lesson_frame, text="Run Code", command=run_user_code).pack(pady=(0,10))

            ctk.CTkLabel(lesson_frame, text="Task:", font=("Helvetica",14,"bold")).pack(anchor="w", pady=(10, 0))
            ctk.CTkLabel(lesson_frame, text=lesson.get("task_instruction", ""), wraplength=520, justify="left").pack(anchor="w")

            check_feedback = ctk.CTkLabel(lesson_frame, text="", font=("Helvetica",12))
            check_feedback.pack(pady=(5,10))

            submit_btn = ctk.CTkButton(lesson_frame, text="Submit Answer")
            submit_btn.pack(pady=(0, 5))

            next_btn = ctk.CTkButton(lesson_frame, text="Next Lesson")
            next_btn.pack_forget()

            lesson_completed = [False]

            def check_output():
                code = code_text.get("1.0", "end").strip()
                try:
                    import io, sys
                    buffer = io.StringIO()
                    sys_stdout = sys.stdout
                    sys.stdout = buffer

                    exec(code, {})

                    sys.stdout = sys_stdout
                    output = buffer.getvalue()
                    expected_output = lesson.get("expected_output", "")

                    if output == expected_output:
                        title = lesson["title"]
                        if title not in completed:
                            user_data["xp"] += xp_reward
                            completed.add(title)
                            users_db[user_data["username"]]["xp"] = user_data["xp"]
                            users_db[user_data["username"]].setdefault("completed_lessons", []).append(title)
                            save_users(users_db)

                            # Check if finished all lessons in current level
                            completed_lessons = set(users_db[user_data["username"]].get("completed_lessons", []))
                            with open("lessons.json", "r") as f:
                                all_lessons = json.load(f)

                            current_level = user_data.get("skill_level")
                            level_order = ["Beginner", "Intermediate", "Advanced"]
                            next_level = None

                            if current_level in level_order:
                                level_titles = {l["title"] for l in all_lessons.get(subj, {}).get(current_level, [])}
                                if level_titles.issubset(completed_lessons):
                                    if current_level == "Advanced":
                                        user_data["skill_level"] = "Master"
                                        users_db[user_data["username"]]["skill_level"] = "Master"
                                    else:
                                        idx = level_order.index(current_level)
                                        user_data["skill_level"] = level_order[idx + 1]
                                        users_db[user_data["username"]]["skill_level"] = level_order[idx + 1]
                                    save_users(users_db)

                            if user_data.get("skill_level") == "Master":
                                clear_content()
                                show_learn()
                                return

                        check_feedback.configure(text=f"✅ Correct! +{xp_reward} XP", text_color="green")
                        submit_btn.pack_forget()
                        if current_lesson_idx[0] < len(lessons) - 1:
                            next_btn.pack(pady=5)
                        lesson_completed[0] = True
                    else:
                        check_feedback.configure(
                            text="❌ Output doesn't match.\nExpected:\n" + expected_output,
                            text_color="red"
                        )
                except Exception as e:
                    sys.stdout = sys_stdout
                    check_feedback.configure(text="❌ Error:\n" + traceback.format_exc(), text_color="red")

            submit_btn.configure(command=check_output)

            def load_next():
                if lesson_completed[0] and current_lesson_idx[0] < len(lessons) - 1:
                    current_lesson_idx[0] += 1
                    load_lesson(current_lesson_idx[0])

            next_btn.configure(command=load_next)

            progress_text = f"Lesson {idx+1} of {len(lessons)}"
            if title in completed:
                progress_text += " ✅ Completed"
                submit_btn.pack_forget()
                if current_lesson_idx[0] < len(lessons) - 1:
                    next_btn.pack(pady=5)
                lesson_completed[0] = True
            ctk.CTkLabel(lesson_frame, text=progress_text, font=("Helvetica",12,"italic")).pack()

        load_lesson(current_lesson_idx[0])

    def show_admin_panel():
        clear_content()
        add_home_button(content_frame, main_frame)
        ctk.CTkLabel(content_frame, text="🛠️ Admin Panel", font=("Helvetica",24,"bold")).pack(pady=10)
        ulist = list(load_users().keys())
        sel = ctk.StringVar(value=ulist[0] if ulist else "")
        ctk.CTkOptionMenu(content_frame, values=ulist, variable=sel).pack(pady=5)
        xp_entry = ctk.CTkEntry(content_frame, placeholder_text="New XP"); xp_entry.pack(pady=5)
        def do_xp():
            try:
                n=int(xp_entry.get())
                u=sel.get()
                ud=load_users(); ud[u]["xp"]=n; save_users(ud)
                if u==user_data["username"]: user_data["xp"]=n
                admin_status.configure(text=f"XP of {u} set to {n}", text_color="green")
            except:
                admin_status.configure(text="Invalid XP!", text_color="red")
        ctk.CTkButton(content_frame,text="Update XP",command=do_xp).pack(pady=3)
        streak_entry = ctk.CTkEntry(content_frame, placeholder_text="New Streak")
        streak_entry.pack(pady=5)

        def do_streak():
            try:
                s = int(streak_entry.get())
                u = sel.get()
                ud = load_users()
                ud[u]["streak"] = s
                save_users(ud)
                if u == user_data["username"]:
                    user_data["streak"] = s
                admin_status.configure(text=f"Streak of {u} set to {s}", text_color="green")
            except:
                admin_status.configure(text="Invalid streak value!", text_color="red")

        ctk.CTkButton(content_frame, text="Update Streak", command=do_streak).pack(pady=3)
        def do_reset():
            u=sel.get(); ud=load_users(); ud[u]["streak"]=0; save_users(ud)
            if u==user_data["username"]: user_data["streak"]=0
            admin_status.configure(text=f"Streak of {u} reset.", text_color="green")
        ctk.CTkButton(content_frame,text="Reset Streak",command=do_reset).pack(pady=3)
        ctk.CTkLabel(content_frame,text="Override Date (YYYY-MM-DD):").pack(pady=5)
        de = ctk.CTkEntry(content_frame, placeholder_text="blank = real date"); de.pack(pady=5)
        def set_date():
            global test_date_override
            v=de.get().strip()
            if not v:
                test_date_override=None
                admin_status.configure(text="Date override cleared.", text_color="green")
                return
            try:
                test_date_override=datetime.strptime(v,"%Y-%m-%d").date()
                admin_status.configure(text=f"Date override set to {v}", text_color="green")
            except:
                admin_status.configure(text="Invalid date format!", text_color="red")
        ctk.CTkButton(content_frame,text="Set Date",command=set_date).pack(pady=3)
        admin_status=ctk.CTkLabel(content_frame,text="",font=("Helvetica",12)); admin_status.pack(pady=5)

    nav_buttons = [
        ("Profile", profile_img, show_profile),
        ("Leaderboard", leaderboard_img, show_leaderboard),
        ("Login Rewards", login_img, show_rewards),
        ("Learn", learn_img, show_learn),
        ("Badges", None, show_badges)
    ]
    if user_data["username"]=="admin":
        nav_buttons.append(("Admin Panel", None, show_admin_panel))

    for name, icon, cmd in nav_buttons:
        ctk.CTkButton(sidebar, text=name, image=icon, corner_radius=5, width=160, height=40, hover_color="#5e81ac", command=cmd).pack(pady=6)

    ctk.CTkButton(sidebar, text="Logout", width=160, height=40, fg_color="#d9534f", hover_color="#c9302c", command=logout).pack(pady=20)

    show_learn()

setup_login_frame()
setup_register_frame()
show_home()
app.mainloop()
