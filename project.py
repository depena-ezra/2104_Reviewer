import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, PhotoImage
from datetime import datetime
import json
import os
import random

USER_SETS = 'sets'
ACP_SETS = 'acp_sets'
HISTORY_FOLDER = 'history'


class ThinkUNextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Think U Next: Reviewer")
        
        self.root.attributes('-fullscreen', True)

        self.root.configure(bg="#FEF3E2") 

        self.style = ttk.Style()
        self.style.configure('TButton',
                             font=('Helvetica', 14, 'bold'),
                             padding=10,
                             relief="flat",
                             background="#FEF3E2",  
                             foreground="#470898",
                             borderwidth=0,
                             width=15,
                             height=2)        

        self.style.map('TButton',
                       background=[('active', '#470898'),  
                                   ('!active', '#470898')]) 

        self.create_widgets()
        self.temp_questions = []


    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#FEF3E2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar_frame = tk.Frame(self.main_frame, width=200, bg="#FAB12F", borderwidth=2)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.logo_image = tk.PhotoImage(file="graphics/TUN.LOGO.png")
        self.logo_label = tk.Label(self.sidebar_frame, image=self.logo_image, bg="#FAB12F")
        self.logo_label.pack(pady=80)

        self.button_frame = tk.Frame(self.sidebar_frame, bg="#FAB12F")
        self.button_frame.pack(side=tk.TOP, padx=40)

        self.create_button = ttk.Button(self.button_frame, text="Create Set", command=lambda: self.switch_panel("create"))
        self.create_button.pack(fill=tk.X, pady=10)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Set", command=lambda: self.switch_panel("edit"))
        self.edit_button.pack(fill=tk.X, pady=10)

        self.review_button = ttk.Button(self.button_frame, text="Review Set", command=lambda: self.switch_panel("review"))
        self.review_button.pack(fill=tk.X, pady=10)

        self.history_button = ttk.Button(self.button_frame, text="View History", command=lambda: self.switch_panel("history"))
        self.history_button.pack(fill=tk.X, pady=10)

        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(fill=tk.X, pady=10)

        self.content_frame = tk.Frame(self.main_frame, bg="#FEF3E2")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.home_panel = tk.Frame(self.content_frame, bg="#FEF3E2")
        self.home_panel.pack(fill=tk.BOTH, expand=True)

        try:
            self.image = tk.PhotoImage(file="graphics/TUN.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None  

        if self.image:
            self.image_label = tk.Label(self.home_panel, image=self.image, bg="#FEF3E2")
            self.image_label.pack(pady=(180, 100), expand=True)
        else:
            print("Image could not be loaded.")

        self.create_panel = self.create_set_panel()
        self.edit_panel = self.create_edit_panel()
        self.review_panel = self.create_review_panel()
        self.history_panel = self.create_history_panel()


    def switch_panel(self, panel_name):
        
        self.home_panel.pack_forget()
        self.create_panel.pack_forget()
        self.edit_panel.pack_forget()
        self.review_panel.pack_forget()
        self.history_panel.pack_forget()

        if panel_name == "create":
            self.create_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "edit":
            self.edit_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "review":
            self.review_panel.pack(fill=tk.BOTH, expand=True)
        elif panel_name == "history":
            self.history_panel.pack(fill=tk.BOTH, expand=True)
        else:
            self.home_panel.pack(fill=tk.BOTH, expand=True)

    def create_set_panel(self):
        create_panel = tk.Frame(self.content_frame, bg="#FEF3E2")

        create_label = tk.Label(create_panel, text="Create a New Set", font=('Helvetica', 16, 'bold'), bg="#FEF3E2", fg="#470898")
        create_label.pack(pady=(60, 5))

        self.create_set_name_var = tk.StringVar()

        set_name_label = tk.Label(create_panel, text="Set Name: ", font=('Helvetica', 12), bg="#FEF3E2")
        set_name_label.pack(pady=5)

        set_name_entry = tk.Entry(create_panel, font=('Helvetica', 12), textvariable=self.create_set_name_var)
        set_name_entry.pack(pady=10)

        self.create_questions_frame = tk.Frame(create_panel, bg="#FEF3E2")
        self.create_questions_frame.pack(pady=20)

        self.create_new_question_var = tk.StringVar()
        self.create_new_answer_var = tk.StringVar()

        new_question_label = tk.Label(create_panel, text="New Question: ", font=('Helvetica', 12), bg="#FEF3E2")
        new_question_label.pack(pady=5)

        new_question_entry = tk.Entry(create_panel, font=('Helvetica', 12), textvariable=self.create_new_question_var)
        new_question_entry.pack(pady=5)

        new_answer_label = tk.Label(create_panel, text="New Answer: ", font=('Helvetica', 12), bg="#FEF3E2")
        new_answer_label.pack(pady=5)

        new_answer_entry = tk.Entry(create_panel, font=('Helvetica', 12), textvariable=self.create_new_answer_var)
        new_answer_entry.pack(pady=5)

        add_button = ttk.Button(create_panel, text="Add Question", command=self.set_add_question)
        add_button.pack(pady=10)

        finish_button = ttk.Button(create_panel, text="Finish", command=self.finish_create_set)
        finish_button.pack(pady=20)

        return create_panel

    def set_add_question(self):
        new_question = self.create_new_question_var.get().strip()
        new_answer = self.create_new_answer_var.get().strip()

        if new_question and new_answer:
            set_name = self.create_set_name_var.get().strip()
            if not set_name:
                messagebox.showerror("Error", "Please provide a set name before adding questions.")
                return

            self.temp_questions.append({"question": new_question, "answer": new_answer})

            row = len(self.temp_questions) - 1  

            question_label = tk.Label(self.create_questions_frame, text=f"{row + 1}. {new_question}", font=('Helvetica', 12), bg="#FEF3E2", wraplength=300, anchor="w")
            question_label.grid(row=row, column=0, sticky="w", padx=10)
            answer_label = tk.Label(self.create_questions_frame, text=f"Answer: {new_answer}", font=('Helvetica', 12), bg="#FEF3E2", wraplength=300, anchor="w")
            answer_label.grid(row=row, column=1, sticky="w", padx=10)

            self.create_new_question_var.set("")
            self.create_new_answer_var.set("")
        else:
            messagebox.showerror("Error", "Please provide an answer.")

    def finish_create_set(self):
        set_name = self.create_set_name_var.get().strip()

        if set_name:
            set_file = os.path.join(USER_SETS, f"{set_name}.json")

            if self.temp_questions:
                with open(set_file, 'w') as f:
                    json.dump(self.temp_questions, f, indent=4)

                messagebox.showinfo("Success", f"Set '{set_name}' saved successfully!")

                self.temp_questions = []
            else:
                messagebox.showerror("Error", "Please add at least one question before finishing.")
        else:
            messagebox.showerror("Error", "Please provide a name for the set.")

    def create_edit_panel(self):
        edit_panel = tk.Frame(self.content_frame, bg="#FEF3E2")

        edit_label = tk.Label(edit_panel, text="Edit an Existing Set", font=('Helvetica', 16, 'bold'), bg="#FEF3E2", fg="#470898")
        edit_label.pack(pady=(60, 5))

        set_files = [f for f in os.listdir(USER_SETS) if f.endswith('.json')]
        if set_files:
            set_names = [os.path.splitext(f)[0] for f in set_files]

            self.edit_set_var = tk.StringVar()
            self.edit_set_var.set(set_names[0]) 

            set_dropdown = ttk.Combobox(edit_panel, textvariable=self.edit_set_var, values=set_names, state="readonly", font=('Helvetica', 12))
            set_dropdown.pack(pady=20)

            edit_button = ttk.Button(edit_panel, text="Edit Selected Set", command=self.edit_selected_set)
            edit_button.pack(pady=10)
        else:
            no_sets_label = tk.Label(edit_panel, text="No sets available.", font=('Helvetica', 14, 'bold'), bg="#FEF3E2", fg="#470898")
            no_sets_label.pack(pady=20)

        return edit_panel


    def edit_selected_set(self):
        set_name = self.edit_set_var.get()
        set_file = os.path.join(USER_SETS, f"{set_name}.json")

        with open(set_file, 'r') as f:
            questions = json.load(f)

        for widget in self.edit_panel.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.edit_panel, bg="#FEF3E2", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.edit_panel, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollable_frame = tk.Frame(canvas, bg="#FEF3E2")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.edit_entries = []

        for idx, question in enumerate(questions):
            question_text = question['question']
            answer_text = question['answer']

            question_label = tk.Label(scrollable_frame, text=f"Q{idx + 1}: ", font=('Helvetica', 12), bg="#FEF3E2")
            question_label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")

            question_entry = tk.Entry(scrollable_frame, font=('Helvetica', 12), width=40)
            question_entry.grid(row=idx, column=1, padx=5, pady=5)
            question_entry.insert(0, question_text)
            self.edit_entries.append({"entry": question_entry, "type": "question"})

            answer_label = tk.Label(scrollable_frame, text="Answer: ", font=('Helvetica', 12), bg="#FEF3E2")
            answer_label.grid(row=idx, column=2, padx=5, pady=5, sticky="w")

            answer_entry = tk.Entry(scrollable_frame, font=('Helvetica', 12), width=40)
            answer_entry.grid(row=idx, column=3, padx=5, pady=5)
            answer_entry.insert(0, answer_text)
            self.edit_entries.append({"entry": answer_entry, "type": "answer"})

            delete_button = ttk.Button(scrollable_frame, text="Delete", command=lambda idx=idx: self.delete_question(set_file, idx, questions))
            delete_button.grid(row=idx, column=4, padx=5, pady=5)

        self.new_question_var = tk.StringVar()
        self.new_answer_var = tk.StringVar()

        new_question_label = tk.Label(scrollable_frame, text="New Question: ", font=('Helvetica', 12), bg="#FEF3E2")
        new_question_label.grid(row=len(questions), column=0, padx=5, pady=5, sticky="w")

        new_question_entry = tk.Entry(scrollable_frame, font=('Helvetica', 12), width=40, textvariable=self.new_question_var)
        new_question_entry.grid(row=len(questions), column=1, padx=5, pady=5)

        new_answer_label = tk.Label(scrollable_frame, text="New Answer: ", font=('Helvetica', 12), bg="#FEF3E2")
        new_answer_label.grid(row=len(questions), column=2, padx=5, pady=5, sticky="w")

        new_answer_entry = tk.Entry(scrollable_frame, font=('Helvetica', 12), width=40, textvariable=self.new_answer_var)
        new_answer_entry.grid(row=len(questions), column=3, padx=5, pady=5)

        add_button = ttk.Button(scrollable_frame, text="Add Question", command=lambda: self.add_question(set_file, questions))
        add_button.grid(row=len(questions), column=4, padx=5, pady=5)

    def add_question(self, set_file, questions):
        new_question = self.new_question_var.get().strip()
        new_answer = self.new_answer_var.get().strip()

        if new_question and new_answer:
            questions.append({"question": new_question, "answer": new_answer})

            with open(set_file, 'w') as f:
                json.dump(questions, f, indent=4)

            messagebox.showinfo("Success", "New question added successfully!")

            self.edit_selected_set()
        else:
            messagebox.showerror("Error", "Please provide both a question and an answer.")


    def delete_question(self, set_file, idx, questions):
        del questions[idx]

        with open(set_file, 'w') as f:
            json.dump(questions, f, indent=4)

        messagebox.showinfo("Success", "Question deleted successfully!")

        self.edit_selected_set()  

    def create_review_panel(self):
        USER_SETS = 'sets'
        ACP_SETS = 'acp_sets'
        review_panel = tk.Frame(self.content_frame, bg="#FEF3E2")

        review_label = tk.Label(
            review_panel,
            text="Choose a Set to Review",
            font=('Helvetica', 16, 'bold'),
            bg="#FEF3E2",
            fg="#470898"
        )
        review_label.pack(pady=(60, 50))

        dropdown_frame = tk.Frame(review_panel, bg="#FEF3E2")
        dropdown_frame.pack(pady=10)

        user_set_files = [f[:-5] for f in os.listdir(USER_SETS) if f.endswith('.json')]
        acp_set_files = [f[:-5] for f in os.listdir(ACP_SETS) if f.endswith('.json')]

        user_set_label = tk.Label(
            dropdown_frame,
            text="User Sets:",
            font=('Helvetica', 12),
            bg="#FEF3E2"
        )
        user_set_label.grid(row=0, column=0, padx=50, pady=5, sticky="n")

        self.set_var = tk.StringVar()
        self.set_var.set(user_set_files[0] if user_set_files else "No user sets available")

        user_set_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.set_var,
            values=user_set_files,
            state="readonly" if user_set_files else "disabled",
            font=('Helvetica', 12),
            width=25
        )
        user_set_dropdown.grid(row=1, column=0, padx=50, pady=5)

        start_user_review_button = ttk.Button(
            dropdown_frame,
            text="Review User Sets",
            command=lambda: self.start_review(USER_SETS, self.set_var.get())
        )
        start_user_review_button.grid(row=2, column=0, padx=50, pady=10)

        acp_set_label = tk.Label(
            dropdown_frame,
            text="ACP Sets:",
            font=('Helvetica', 12),
            bg="#FEF3E2"
        )
        acp_set_label.grid(row=0, column=1, padx=50, pady=5, sticky="n")

        self.acp_set_var = tk.StringVar()
        self.acp_set_var.set(acp_set_files[0] if acp_set_files else "No ACP sets available")

        acp_set_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.acp_set_var,
            values=acp_set_files,
            state="readonly" if acp_set_files else "disabled",
            font=('Helvetica', 12),
            width=25
        )
        acp_set_dropdown.grid(row=1, column=1, padx=10, pady=5)

        start_acp_review_button = ttk.Button(
            dropdown_frame,
            text="Review ACP Sets",
            command=lambda: self.start_review(ACP_SETS, self.acp_set_var.get())
        )
        start_acp_review_button.grid(row=2, column=1, padx=10, pady=10)

        return review_panel

    def start_review(self, folder, set_name):
        if set_name == "No user sets available" or set_name == "No ACP sets available":
            tk.messagebox.showerror("Error", "No valid set selected for review.")
            return

        set_file = os.path.join(folder, f"{set_name}.json")

        try:
            with open(set_file, 'r') as f:
                self.questions = json.load(f)

            random.shuffle(self.questions)

            for widget in self.review_panel.winfo_children():
                widget.destroy()

            self.current_question_index = 0
            self.mistakes = []
            self.display_question()
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"Set file not found: {set_file}")
        except json.JSONDecodeError:
            tk.messagebox.showerror("Error", f"Failed to load set file: {set_file}")


    def display_question(self):
        for widget in self.review_panel.winfo_children():
            widget.destroy()

        if self.current_question_index >= len(self.questions):
            self.show_review_result(set_name=self.set_var.get())
            return

        question_data = self.questions[self.current_question_index]
        question_text = question_data["question"]
        self.correct_answer = question_data["answer"]

        question_label = tk.Label(
            self.review_panel,
            text=f"{question_text}",
            font=('Helvetica', 20, 'bold'),
            bg="#FEF3E2",
        )
        question_label.pack(pady=(220, 20))

        answer_frame = tk.Frame(self.review_panel, bg="#FEF3E2")
        answer_frame.pack(pady=10)

        self.user_answer_entry = tk.Text(answer_frame, font=('Helvetica', 15), height=5, width=60)
        self.user_answer_entry.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(answer_frame, command=self.user_answer_entry.yview)
        scrollbar.pack(side="right", fill="y")

        self.user_answer_entry.config(yscrollcommand=scrollbar.set)

        confirm_button = ttk.Button(self.review_panel, text="Confirm Answer", command=self.validate_answer)
        confirm_button.pack(pady=20)


    def validate_answer(self):
        print("Confirm Answer button clicked!")

        user_answer = self.user_answer_entry.get("1.0", tk.END).strip()  

        for widget in self.review_panel.winfo_children():
            widget.destroy()

        feedback_label = tk.Label(
            self.review_panel,
            text="",
            font=('Helvetica', 30),
            bg="#FEF3E2",
        )

        if user_answer.lower() == self.correct_answer.lower():
            feedback_label.config(text="Correct!", fg="green")
        else:
            feedback_label.config(
                text=f"Incorrect! The correct answer was: {self.correct_answer}",
                fg="red",
            )
            self.mistakes.append({
                "question": self.questions[self.current_question_index]["question"],
                "user_answer": user_answer,
                "answer": self.correct_answer,
            })

        feedback_label.pack(pady=220)

        next_button = ttk.Button(self.review_panel, text="Next Question", command=self.next_question)
        next_button.pack(pady=20)

    def next_question(self):
        self.current_question_index += 1
        self.display_question()

    def show_review_result(self, set_name):
        for widget in self.review_panel.winfo_children():
            widget.destroy()

        total_questions = len(self.questions)
        score = total_questions - len(self.mistakes)

        result_label = tk.Label(
            self.review_panel,
            text=f"Your Score: {score}/{total_questions}",
            font=('Helvetica', 30, 'bold'),
            bg="#FEF3E2"
        )
        result_label.pack(pady=(220, 20))

        if score == total_questions:
            message_label = tk.Label(
                self.review_panel,
                text="Perfect score! Well done!",
                font=('Helvetica', 14),
                bg="#FEF3E2"
            )
            message_label.pack(pady=10)
        else:
            message_label = tk.Label(
                self.review_panel,
                text="Review the mistakes below:",
                font=('Helvetica', 14),
                bg="#FEF3E2"
            )
            message_label.pack(pady=10)

            for mistake in self.mistakes:
                mistake_text = (
                    f"Question: {mistake['question']}\n"
                    f"Your Answer: {mistake['user_answer']}\n"
                    f"Correct Answer: {mistake['answer']}"
                )
                mistake_label = tk.Label(
                    self.review_panel,
                    text=mistake_text,
                    font=('Helvetica', 12),
                    bg="#FEF3E2",
                    justify="left"
                )
                mistake_label.pack(pady=5)

        self.save_progress(set_name, score, self.mistakes)


    def save_progress(self, set_name, score, mistakes):
        if not os.path.exists(HISTORY_FOLDER):
            os.makedirs(HISTORY_FOLDER)

        session_data = {
            "set_name": set_name,
            "score": score,
            "mistakes": mistakes,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        history_filename = os.path.join(HISTORY_FOLDER, f"{set_name.upper()}_session_{timestamp}.json")

        with open(history_filename, 'w') as f:
            json.dump(session_data, f, indent=4)
        
    def create_history_panel(self):
        history_panel = tk.Frame(self.content_frame, bg="#FEF3E2")

        history_label = tk.Label(history_panel, text="Review History", font=('Helvetica', 16, 'bold'), bg="#FEF3E2", fg="#470898")
        history_label.pack(pady=(60, 5))

        history_files = [f for f in os.listdir(HISTORY_FOLDER) if f.endswith('.json')]

        if not history_files:
            no_history_label = tk.Label(history_panel, text="No review history available.", font=('Helvetica', 14, 'bold'), bg="#FEF3E2", fg="#470898")
            no_history_label.pack(pady=20)
        else:
            set_names = list(set(file.split('_')[0] for file in history_files))  
            set_combo = ttk.Combobox(history_panel, values=set_names, state="readonly", font=('Helvetica', 12))
            set_combo.set("Select a Set") 
            set_combo.pack(pady=10)

            history_tree = ttk.Treeview(history_panel, columns=("Date", "Score", "Mistakes"), show="headings", height=20)

            history_tree.heading("Date", text="Date")
            history_tree.heading("Score", text="Score")
            history_tree.heading("Mistakes", text="Mistakes")

            history_tree.column("Date", width=350, anchor="center")
            history_tree.column("Score", width=300, anchor="center")
            history_tree.column("Mistakes", width=350, anchor="center")

            history_tree.pack(pady=10)

            def filter_history(event):
                selected_set = set_combo.get()
                if selected_set != "Select a Set":
                    filtered_files = [f for f in history_files if f.split('_')[0] == selected_set]

                    for row in history_tree.get_children():
                        history_tree.delete(row)

                    for file in filtered_files:
                        file_path = os.path.join(HISTORY_FOLDER, file)
                        try:
                            with open(file_path, 'r') as f:
                                session_data = json.load(f)

                            date = session_data.get('date', 'Unknown Date')
                            score = f"{session_data.get('score', 0)}"
                            mistakes_count = len(session_data.get('mistakes', []))

                            history_tree.insert("", "end", values=(date, score, mistakes_count))

                        except Exception as e:
                            print(f"Error reading file {file}: {e}")
                            continue

            set_combo.bind("<<ComboboxSelected>>", filter_history)

            def show_history_details(event):
                selected_item = history_tree.selection()
                if selected_item:
                    selected_file = os.path.join(HISTORY_FOLDER, history_files[history_tree.index(selected_item[0])])

                    try:
                        with open(selected_file, 'r') as f:
                            session_data = json.load(f)

                        for widget in history_panel.winfo_children():
                            if isinstance(widget, tk.Label) and widget != history_label:
                                widget.destroy()

                        details_label = tk.Label(history_panel, text=f"Date: {session_data['date']}\nScore: {session_data['score']}", font=('Helvetica', 12), bg="#FEF3E2")
                        details_label.pack(pady=10)

                        if session_data['mistakes']:
                            mistakes_label = tk.Label(history_panel, text="Mistakes:", font=('Helvetica', 12, 'bold'), bg="#FEF3E2")
                            mistakes_label.pack(pady=10)

                            for mistake in session_data['mistakes']:
                                question = mistake.get('question', 'No question provided')
                                user_answer = mistake.get('user_answer', 'No answer provided')
                                correct_answer = mistake.get('answer', 'No correct answer provided')

                                mistake_text = (
                                    f"Question: {question}\n"
                                    f"Your Answer: {user_answer}\n"
                                    f"Correct Answer: {correct_answer}"
                                )
                                mistake_label = tk.Label(
                                    history_panel,
                                    text=mistake_text,
                                    font=('Helvetica', 10),
                                    bg="#FEF3E2",
                                    justify="left"
                                )
                                mistake_label.pack(pady=5)
                        else:
                            no_mistakes_label = tk.Label(history_panel, text="No mistakes! Well done!", font=('Helvetica', 12, 'bold'), bg="#FEF3E2")
                            no_mistakes_label.pack(pady=10)

                    except Exception as e:
                        print(f"Error reading session details from {selected_file}: {e}")

            history_tree.bind("<Double-1>", show_history_details)

        return history_panel


    def exit_program(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ThinkUNextApp(root)
    root.mainloop()
