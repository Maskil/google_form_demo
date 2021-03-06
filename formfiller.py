from tkinter import *
import tkinter.scrolledtext as st
import json
import time
from bs4 import BeautifulSoup
import lxml.html as LH
from selenium import webdriver
import smtplib


# writes and reads
def writeURL():
    js = json.dumps(urls)
    file = open('urls.txt', 'w')
    file.write(js)
    file.close()


def readURL():
    global urls
    try:
        file = open('urls.txt', 'r')
        urls = {}
        js = file.read()
        urls = json.loads(js)
        file.close()
    except:
        file = open('urls.txt', 'a')
        urls = {}


def writeRecord():
    js = json.dumps(records)
    file = open('records.txt', 'w')
    file.write(js)
    file.close()


def readRecord():
    global records
    try:
        file = open('records(tmp).txt', 'r')
        records = {}
        js = file.read()
        records = json.loads(js)
        file.close()
    except:
        records = open('records(tmp).txt', 'a')
        records = {}


def writeChrome():
    js = json.dumps(chromedriverLocation)
    file = open('chromedriver_locations.txt', 'w')
    file.write(js)
    file.close()


def readChrome():
    global chromedriverLocation
    try:
        file = open('chromedriver_locations.txt', 'r')
        chromedriverLocation = {}
        js = file.read()
        chromedriverLocation = json.loads(js)
        file.close()
    except:
        file = open('chromedriver_locations.txt', 'a')
        chromedriverLocation = {}


def writeU():
    js = json.dumps(usernames)
    file = open('usernames.txt', 'w')
    file.write(js)
    file.close()


def readU():
    global usernames
    try:
        file = open('usernames.txt', 'r')
        usernames = {}
        js = file.read()
        usernames = json.loads(js)
        file.close()
    except:
        file = open('usernames.txt', 'a')
        usernames = {}


def writeanswers():
    js = json.dumps(recorded_answers)
    file = open('records(answers).txt', 'w')
    file.write(js)
    file.close()


def readanswers():
    global recorded_answers
    try:
        file = open('records(answers).txt', 'r')
        recorded_answers = {}
        js = file.read()
        recorded_answers = json.loads(js)
        file.close()
    except:
        file = open('records(answers).txt', 'a')
        recorded_answers = {}


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        Frame.__init__(self, container, bd=4, relief=SUNKEN)
        canvas = Canvas(self, borderwidth=0)
        self.scrollable_frame = Frame(canvas)
        scrollbar = Scrollbar(self, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.create_window((3, 3), window=self.scrollable_frame, anchor=NW, tags="self.scrollable_frame")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox(ALL)))

        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)


def login_window(root, driver, nickname, link, current_page):
    root.title('Login')
    container = Frame(bd=3, relief=SUNKEN)
    email_input = StringVar()
    password_input = StringVar()
    error = StringVar()
    def login(email, password):
        if email == '':
            error.set('Empty Input')
            return
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # or 465.
            smtpObj.ehlo()  # setup.
            smtpObj.starttls()  # encryption.
            smtpObj.login(email, password)
        except:
            error.set('Invalid Input.')
            return
        tmpurl = driver.current_url
        driver.find_element_by_name("identifier").send_keys(email)
        driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
        while tmpurl == driver.current_url:
            time.sleep(0.5)
        tmpurl = driver.current_url
        while True:
            try:
                driver.find_element_by_name("password").send_keys(password)
                driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
                break
            except:
                continue
        while tmpurl == driver.current_url:
            time.sleep(0.5)
        if nickname != 'tmp':
            readU()
            usernames[nickname] = {'email':email,'password':password}
            writeU()
        container.destroy()
        formanswer(root, driver, nickname, link, current_page)

    def show_unshow():
        if password_label.cget("show") == '*':
            password_label.config(show='')
        else:
            password_label.config(show='*')

    Label(container, font=midfont, fg='red', textvariable=error).pack(side=BOTTOM, anchor=W)
    Label(container, font=bigfont, text="Login").pack()
    Label(container, font=midfont, text="You need to Log into your Google account to answer this form.").pack()
    Label(container, font=midfont, text="It might take some time to login, please be patient.").pack()
    emlpsw_frame = LabelFrame(container, font=midfont, text="Google Account")
    eml_frame = LabelFrame(emlpsw_frame, font=midfont, text="Email Address")
    Entry(eml_frame, font=midfont, width=30, textvariable=email_input).pack(fill=X)
    psw_frame = LabelFrame(emlpsw_frame, font=midfont, text="Password")
    password_label = Entry(psw_frame, font=midfont, show='*', width=30, textvariable=password_input)
    password_label.pack(fill=X)
    bottomframe = Frame(emlpsw_frame)
    email_button = Button(bottomframe, font=midfont, text="Login", command=lambda: login(email_input.get(), password_input.get()))
    email_button.pack(side=RIGHT, padx=2, pady=2)
    Button(bottomframe, font=midfont, text="(un)show password", command=lambda: show_unshow()).pack(side=RIGHT, padx=2, pady=2)
    eml_frame.pack(side=TOP, anchor=W)
    psw_frame.pack(side=TOP, anchor=W)
    bottomframe.pack(side=BOTTOM, fill=X, padx=2, pady=2)
    emlpsw_frame.pack()
    container.pack(side=BOTTOM, fill=BOTH, expand=True)


def formanswer(root, driver, nickname, link, current_page):
    readRecord()
    readURL()
    def readdata():
        global shorts, choices, boxes, longs, form_submit, containers, num_of_questions, all_tles, all_ctents, all_types, must_fill_qs, orderRecord, description
        soup = BeautifulSoup(driver.execute_script("return document.documentElement.innerHTML"), features='lxml')
        num_of_questions = len(
            driver.find_elements_by_class_name('freebirdFormviewerComponentsQuestionBaseTitle'))
        shorts = driver.find_elements_by_class_name('quantumWizTextinputPaperinputInput')
        choices = driver.find_elements_by_class_name('appsMaterialWizToggleRadiogroupElContainer')
        boxes = driver.find_elements_by_class_name('quantumWizTogglePapercheckboxInnerBox')
        longs = driver.find_elements_by_class_name('quantumWizTextinputPapertextareaInput')
        form_submit = driver.find_elements_by_class_name('appsMaterialWizButtonPaperbuttonContent')
        tmpShort = 0
        tmpPara = 0
        baseCir = 0
        baseBox = 0
        orderRecord = []
        must_fill_qs = []
        top_pages = []
        answer_pages = []
        all_tles = []
        all_ctents = []
        all_types = []
        root1 = LH.fromstring(str(soup.find("div", {"class": "freebirdFormviewerViewHeaderTitle", "role": "heading"})))
        for elt in root1.xpath('//div'):
            root.title(elt.text_content())
        questions_father = soup.find_all("div",
                                         {"class": "freebirdFormviewerComponentsQuestionBaseHeader"})
        containers = soup.find("div", {"class": "freebirdFormviewerViewItemList", "role": "list"}).findChildren("div", {
            "role": "listitem"}, recursive=False)
        for j, each in enumerate(containers):
            if 'm2' not in str(each):
                containers.pop(j)
        formatSequence = []
        for each in soup.find_all(type='hidden'):
            formatSequence.append(str(each)) if ('year' in str(each) or 'month' in str(each) or 'day' in str(
                each)) and len(formatSequence) <= 2 else None
        questionTitles = []
        answerEntries = []
        for each in questions_father:
            questionsHTMLTitle = each.findChildren("div", {"role": "heading"}, recursive=True)
            tmp = questionsHTMLTitle
            root1 = LH.fromstring(str(tmp[0]))
            for elt in root1.xpath('//div'):
                questionTitles.append(elt.text_content())
        for each in containers:
            label = []
            label.append(each.findChildren("input", {"class": "quantumWizTextinputPaperinputInput"}, recursive=True))
            label.append(
                each.findChildren("div", {"class": "appsMaterialWizToggleRadiogroupElContainer"}, recursive=True))
            label.append(
                each.findChildren("div", {"class": "quantumWizTogglePapercheckboxCheckMarkContainer"}, recursive=True))
            label.append(
                each.findChildren("textarea", {"class": "quantumWizTextinputPapertextareaInput"}, recursive=True))
            label.sort()
            if len(label[-1]) != 0:
                answerEntries.append(label[-1][0])
        for i, value in enumerate(answerEntries):
            qsctent = []
            numOfctent = 0
            qstype = ''
            qstle = f"{questionTitles[i]}" + ("(Must fill)" if questionTitles[i][-1] == "*" else "")
            if '*(Must fill)' in qstle: must_fill_qs.append(i)
            if 'quantumWizTextinputPaperinputInput' in str(value) and not ('maxlength="2"' in str(value)):
                if 'type="date"' in str(value):
                    qsctent.append(f"Answer a date. Format: Your default date foramt. Check on your Chrome if you are not sure.")
                    qsctent.append(
                        "If your default date format is mm/dd/yyyy, only type mmddyyyy. Do not type any symbols.")
                    orderRecord.append(tmpShort)
                    tmpShort += 1
                    qstype = 'date'
                else:
                    qsctent.append("Answer in one line.")
                    orderRecord.append(tmpShort)
                    tmpShort += 1
                    qstype = 'short'
            elif 'maxlength="2"' in str(value):
                qsctent.append("Answer a time. Format: HH:mm.  Note: HH means 24-hour")
                orderRecord.append(tmpShort)
                tmpShort += 2
                qstype = 'time'
            elif 'quantumWizTextinputPapertextareaInput' in str(value):
                qsctent.append("Answer a paragraph.")
                orderRecord.append(tmpPara)
                tmpPara += 1
                qstype = 'long'
            elif 'appsMaterialWizToggleRadiogroupElContainer' in str(value) and len(
                    containers[i].findChildren("div", {"class": "freebirdMaterialScalecontentLabel"}, recursive=True)) > 0:
                label = containers[i].findChildren("div", {"class": "freebirdMaterialScalecontentRangeLabel"}, recursive=True)
                tmp_soup = BeautifulSoup(str(label[0]), features='lxml')
                tmp_soup1 = BeautifulSoup(str(label[1]), features='lxml')
                qsctent.append(f"{tmp_soup.div.string} ↑ ")
                label = containers[i].findChildren("div", {"class": "freebirdMaterialScalecontentLabel"}, recursive=True)
                for j, each in enumerate(label):
                    tmp_soup = BeautifulSoup(str(each), features='lxml')
                    qsctent.append(f"({j + 1}) {tmp_soup.div.string}")
                qsctent.append(f"{tmp_soup1.div.string} ↓")
                qsctent.append('Answer a number.')
                orderRecord.append(baseCir)
                baseCir += len(label)
                numOfctent = len(label)
                qstype = 'label'
            elif 'appsMaterialWizToggleRadiogroupElContainer' in str(value) and len(
                    containers[i].findChildren("div", {"class": "freebirdMaterialScalecontentLabel"}, recursive=True)) == 0:
                label = containers[i].findChildren("span", {"class": "docssharedWizToggleLabeledLabelText"}, recursive=True)
                for j, each in enumerate(label):
                    tmp_soup = BeautifulSoup(str(each), features='lxml')
                    qsctent.append(f"({j + 1}) {tmp_soup.span.string}")
                qsctent.append('Answer a number.')
                orderRecord.append(baseCir)
                baseCir += len(label)
                numOfctent = len(label)
                qstype = 'choice'
            elif 'quantumWizTogglePapercheckboxCheckMarkContainer' in str(value):
                label = containers[i].findChildren("span", {"class": "freebirdFormviewerComponentsQuestionCheckboxLabel"}, recursive=True)
                for j, each in enumerate(label):
                    tmp_soup = BeautifulSoup(str(each), features='lxml')
                    qsctent.append(f"□({j + 1}) {tmp_soup.span.string}")
                qsctent.append('Answer one or multiple numbers with commas. Ex: 1,2,3 or 1, 2, 3')
                orderRecord.append(baseBox)
                baseBox += len(label)
                numOfctent = len(label)
                qstype = 'box'
            label = [qstle, qsctent]
            top_pages.append(label)
            answer_pages.append(qstype)
            all_tles.append(qstle)
            all_ctents.append(qsctent)
            all_types.append(qstype)
            readRecord()
            records[nickname] = {'titles': all_tles, 'contents': all_ctents, 'types': all_types}
            writeRecord()

    def magic():
        def submit_form():
            submit_pass = True
            for each in must_fill_qs:
                for every in notanswered:
                    if each == every:
                        submit_pass = False
                        error.set('MUST FILL question(s) not filled yet')
                        return
            if submit_pass:
                form_submit[-1].click()
                if len(driver.find_elements_by_class_name('freebirdFormviewerComponentsQuestionBaseTitle')) == 0:
                    def goodbye():
                        for widget in root.winfo_children():
                            widget.destroy()
                        main(root, driver)
                    for widget in root.winfo_children():
                        widget.destroy()
                    Label(font=bigfont, text='Form submitted.').pack(expand=True)
                    Button(font=bigfont, text='Go back to Hangar', command=lambda: goodbye()).pack(expand=True)
                    driver.close()
                else:
                    for widget in root.winfo_children():
                        widget.destroy()
                    current_page.set(current_page.get() + 1)
                    formanswer(root, driver, nickname, link, current_page)

        def submit():
            qsType = records[nickname]['types'][current_question.get() - 1]
            qsPos = orderRecord[current_question.get() - 1]
            if answer_input.get() == '' and qsType != 'long':
                error.set('Empty Input')
                return
            if qsType == 'long':
                answer_input.set(long.get('1.0', END))
                if answer_input.get() == '':
                    return
                longs[qsPos].send_keys(answer_input.get())
                btn.config(state=DISABLED)
                long.config(state=DISABLED)
                notanswered.remove(current_question.get() - 1)
                answer_record[current_question.get()] = {'answer': answer_input.get(), 'type': 'long','location':qsPos}
            elif qsType == 'date':
                if not 8 == len(answer_input.get()):
                    error.set('Invalid Date Input')
                else:
                    shorts[qsPos].send_keys(answer_input.get())
                    btn.config(state=DISABLED)
                    short.config(state=DISABLED)
                    notanswered.remove(current_question.get() - 1)
                    answer_record[current_question.get()] = {'answer': answer_input.get(), 'type': 'date','location':qsPos}
            elif qsType == 'time':
                s = answer_input.get().replace(' ', '').split(':', 1)
                if 24 > int(s[0]) >= 0 and 59 >= int(s[1]) > 0:
                    shorts[qsPos].send_keys(s[0])
                    shorts[qsPos + 1].send_keys(s[1])
                    btn.config(state=DISABLED)
                    short.config(state=DISABLED)
                    notanswered.remove(current_question.get() - 1)
                    answer_record[current_question.get()] = {'answer': [s[0], s[1]], 'type': 'time','location':[qsPos,qsPos+1]}
                else:
                    error.set('Invalid Time Input')
            elif qsType == 'choice' or qsType == 'label':
                try:
                    int(answer_input.get())
                except:
                    error.set('Not a number')
                    return
                if qsType == 'choice':
                    if int(answer_input.get()) > len(records[nickname]['contents'][current_question.get() - 1]) - 1 or int(answer_input.get()) < 1:
                        error.set('Input out of range')
                        return
                else:
                    if int(answer_input.get()) > len(records[nickname]['contents'][current_question.get() - 1]) - 3 or int(answer_input.get()) < 1:
                        error.set('Input out of range')
                        return
                choices[qsPos + int(answer_input.get()) - 1].click()
                btn.config(state=DISABLED)
                short.config(state=DISABLED)
                notanswered.remove(current_question.get() - 1)
                answer_record[current_question.get()] = {'answer': int(answer_input.get()), 'type': 'choice' if qsType == 'choice' else 'label','location': qsPos + int(answer_input.get()) - 1}
            elif qsType == 'box':
                s = answer_input.get().replace(' ', '').split(',')
                for each in s:
                    try:
                        int(each)
                    except:
                        error.set('Not a number')
                        return
                box_pass = True
                for each in s:
                    if not (len(records[nickname]['contents'][current_question.get()-1]) >= int(each) >= 1):
                        box_pass = False
                        error.set('Input out of range')
                        break
                if box_pass:
                    answerlabel = []
                    locationlabel = []
                    for each in s:
                        boxes[qsPos + int(each) - 1].click()
                        answerlabel.append(int(each))
                        locationlabel.append(qsPos + int(each) - 1)
                    btn.config(state=DISABLED)
                    short.config(state=DISABLED)
                    notanswered.remove(current_question.get() - 1)
                    answer_record[current_question.get()] = {'answer':answerlabel,'type':'box','location': locationlabel}
            else:
                shorts[qsPos].send_keys(answer_input.get())
                btn.config(state=DISABLED)
                short.config(state=DISABLED)
                notanswered.remove(current_question.get() - 1)
                answer_record[current_question.get()] = {'answer':answer_input.get(),'type':'short','location':qsPos}
            if nickname != 'tmp':
                readanswers()
                tmpdic = dict(sorted(answer_record.items(),key=lambda item:item[0]))
                recorded_answers[nickname][int(current_page.get())] = tmpdic
                writeanswers()
        nonlocal questionframe, answerframe, answer_record
        error = StringVar()
        answer_input = StringVar()
        answerframe.destroy()
        answerframe = Frame(root, bd=3, relief=SUNKEN, height=265)
        answerframe.pack_propagate(False)
        answerframe.pack(side=BOTTOM, fill=BOTH, expand=True)

        Label(answerframe, textvariable=error, fg='red').pack(side=BOTTOM, anchor=W)

        if records[nickname]['types'][current_question.get() - 1] == 'long':
            long = st.ScrolledText(answerframe, font=smallfont, width=90, height=16)
            long.place(x=5, y=5)
        else:
            short = Entry(answerframe, font=smallfont, width=70, textvariable=answer_input)
            short.place(x=5, y=5)
        if '*(Must fill)' in records[nickname]['titles'][current_question.get() - 1][-12:]:
            Label(answerframe, font=smallfont, fg='red', text='*Must Fill').place(x=680, y=5)
        btn = Button(answerframe, font=smallfont, text='Confirm', command=lambda: submit())
        btn.place(x=670, y=30)
        if current_question.get() == total_question.get():
            Button(answerframe, font=smallfont, text='Next Page' if urls[nickname]['pages'] > current_page.get() else 'Submit', command=lambda: submit_form()).place(x=670, y=25 * 2.5)

        questionframe.destroy()
        questionframe = ScrollableFrame(root)
        questionframe.pack(side=BOTTOM, fill=BOTH, expand=True)
        tlepack = Label(questionframe.scrollable_frame, font=smallfont, wraplength=root.winfo_width()-50, justify=LEFT, text=all_tles[current_question.get() - 1])
        tlepack.pack(side=TOP, anchor=W)
        for each in all_ctents[current_question.get() - 1]:
            Label(questionframe.scrollable_frame, font=smallfont, text=each).pack(side=TOP, anchor=W)

    def next_page():
        current_question.set(current_question.get() + 1)
        question_num_rec.set(f'Question {current_question.get()}/{total_question.get()}')
        if current_question.get() == total_question.get():
            next_button.config(state=DISABLED)
            prev_button.config(state=NORMAL)
        else:
            prev_button.config(state=NORMAL)
        magic()

    def prev_page():
        current_question.set(current_question.get() - 1)
        question_num_rec.set(f'Question {current_question.get()}/{total_question.get()}')
        if current_question.get() == 1:
            prev_button.config(state=DISABLED)
            next_button.config(state=NORMAL)
        else:
            next_button.config(state=NORMAL)
        magic()

    answerframe = Frame(root, bd=3, relief=SUNKEN, height=265)
    questionframe = ScrollableFrame(root)
    question_num_rec = StringVar()
    current_question = IntVar()
    current_question.set(1)
    answer_record = {}
    readdata()
    notanswered = []

    bottomframe = Frame()
    bottomframe.pack(side=BOTTOM, fill=X, expand=False)
    next_button = Button(bottomframe, font=smallfont, text=" → ", command=next_page)
    prev_button = Button(bottomframe, font=smallfont, text=" ← ", command=prev_page)
    next_button.pack(side=RIGHT)
    prev_button.pack(side=RIGHT)
    Label(bottomframe, font=smallfont, fg='purple', text='Author: A 2021 graduate').pack(side=LEFT)
    prev_button.config(state=DISABLED)
    total_question = IntVar()
    total_question.set(num_of_questions)
    if current_question.get() == total_question.get() and total_question.get() == 1:
        prev_button.config(state=DISABLED)
        next_button.config(state=DISABLED)
    else:
        prev_button.config(state=DISABLED)
    question_num_rec.set(f'Question {current_question.get()}/{total_question.get()}')
    Label(bottomframe, font=smallfont, textvariable=question_num_rec).pack(side=BOTTOM)
    for i in range(num_of_questions):
        notanswered.append(i)
    magic()


def auto(root,driver,nickname):
    root.title('Final Confirm')
    confirm_frame = Frame(bd=3,relief=SUNKEN)
    readU()
    flag=True
    for each in usernames:
        if each == nickname:
            flag=False
            Label(confirm_frame,font=midfont,text='Google Account').pack(side=TOP,anchor=NW)
            Label(confirm_frame,font=midfont,text=usernames[each]['email']).pack(side=TOP,anchor=NW)
            Label(confirm_frame, font=midfont, text=usernames[each]['password']).pack(side=TOP, anchor=NW)
    if flag:
        Label(confirm_frame, font=midfont, fg='orange',text='Fill without a Google Account').pack(side=TOP, anchor=NW)
    Label(confirm_frame,font=midfont,text='').pack()
    readanswers()
    for value,key in recorded_answers[nickname].items():
        Label(confirm_frame, font=midfont, text=f"#{value} Page").pack(side=TOP, anchor=NW)
        tmp_frame = Frame(confirm_frame,bd=2,relief=SUNKEN)
        for value1,key1 in key.items():
            Label(tmp_frame, font=midfont, justify=LEFT,text=f"{value1}: {key1['answer'][0:-1] if key1['type'] == 'long' else key1['answer']}").pack(side=TOP, anchor=NW)
        tmp_frame.pack(side=TOP, anchor=NW)
        Label(confirm_frame,text='').pack()

    def finished():
        def goodbye():
            confirm_frame.destroy()
            main(root, driver)
        for widget in confirm_frame.winfo_children():
            widget.destroy()
        driver.close()
        Label(confirm_frame,font=bigfont,text='Auto-fill finished.').pack(expand=True)
        Button(confirm_frame,font=bigfont,text='Go back to Hangar',command=lambda :goodbye()).pack(expand=True)


    def execute():
        if not flag:
            readU()
            tmpurl = driver.current_url
            driver.find_element_by_name("identifier").send_keys(usernames[nickname]['email'])
            driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
            while tmpurl == driver.current_url:
                time.sleep(0.5)
            tmpurl = driver.current_url
            while True:
                try:
                    driver.find_element_by_name("password").send_keys(usernames[nickname]['password'])
                    driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
                    break
                except:
                    continue
            while tmpurl == driver.current_url:
                time.sleep(0.5)
        readURL()
        readanswers()
        lis = []
        answered = []
        tmp = 1
        for value, key in recorded_answers[nickname].items(): answered.append(value)
        while len(answered) > 0:
            if int(answered[0]) == tmp:
                lis.append(answered[0])
                answered.remove(answered[0])
            else:
                lis.append(0)
            tmp += 1
        for i in range(urls[nickname]['pages']-len(lis)): lis.append(0)
        driver.refresh()
        for each in lis:
            if each == 0:
                driver.find_elements_by_class_name('appsMaterialWizButtonPaperbuttonContent')[-1].click()
            else:
                shorts = driver.find_elements_by_class_name('quantumWizTextinputPaperinputInput')
                choices = driver.find_elements_by_class_name('appsMaterialWizToggleRadiogroupElContainer')
                boxes = driver.find_elements_by_class_name('quantumWizTogglePapercheckboxInnerBox')
                longs = driver.find_elements_by_class_name('quantumWizTextinputPapertextareaInput')
                for value,key in recorded_answers[nickname][each].items():
                    if key['type'] == 'short': shorts[key['location']].send_keys(key['answer'])
                    if key['type'] == 'long': longs[key['location']].send_keys(key['answer'])
                    if key['type'] == 'choice' or key['type'] == 'label': choices[key['location']].click()
                    if key['type'] == 'box':
                        for each in key['location']:
                            boxes[each].click()
                driver.find_elements_by_class_name('appsMaterialWizButtonPaperbuttonContent')[-1].click()
        finished()


    Button(confirm_frame,font=bigfont,text='Confirm',command=lambda :execute()).pack(side=BOTTOM,anchor=E)
    confirm_frame.pack(side=BOTTOM,fill=BOTH,expand=True)


def main(root, driver):
    root.title('Hangar')
    root.wm_geometry('750x600')
    frame = Frame(bd=3, relief=SUNKEN)
    frame.pack(side=BOTTOM, fill=BOTH, expand=True)
    error = StringVar()
    nickname = StringVar()
    url = StringVar()
    current_page = IntVar()
    current_page.set(1)
    Label(frame, font=midfont, fg='orange', textvariable=error).pack(side=BOTTOM, anchor=W)
    Label(frame, font=bigfont, text="Before we start, you need to be clear with:").pack()
    message = '''#1. Make sure you have read README file. It could be hard to troubleshoot without it.\n#2. This program is only for your ease. If it is not convenient as you have expected, delete it.\nContact Author: hg5180028@hiroogakuen.com '''
    Label(frame, font=midfont, wraplength=750, text=message).pack()
    Label(frame, font=midfont, text='').pack()
    nameorlink = LabelFrame(frame, font=midfont, text='Type the nickname or URL of the form')
    namelabel = LabelFrame(nameorlink, font=midfont, text='Name')
    Entry(namelabel, font=midfont, width=20, textvariable=nickname).pack()
    urllabel = LabelFrame(nameorlink, font=midfont, text='URL')
    Entry(urllabel, font=midfont, width=80, textvariable=url).pack()
    namelabel.pack(side=TOP, anchor=NW, padx=2, pady=2)
    urllabel.pack(side=TOP, anchor=NW, padx=2, pady=2)
    nameorlink.pack()
    readURL()
    if 'tmp' in urls:
        del urls['tmp']
    writeURL()

    def howmanypages(finalurl, finalname):

        readRecord()

        def changestate():
            if pageflag.get():
                pageinput.configure(state=NORMAL)
            else:
                pageinput.configure(state=DISABLED)
                num_of_pages.set(1)

        def confirm():
            if finalname == 'tmp':
                readURL()
                urls['tmp'] = {'url': finalurl, 'pages': num_of_pages.get()}
                frame.destroy()
                for value, key in urls.items():
                    if key['url'] == finalurl:
                        key['pages'] = num_of_pages.get()
                writeURL()
                if len(driver.find_elements_by_class_name(
                        'freebirdFormviewerComponentsQuestionBaseTitle')) == 0 or driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent"):
                    try:
                        driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent")[-1].click()
                    except:
                        pass
                    login_window(root, driver, finalname, finalurl, current_page)
                else:
                    formanswer(root, driver, finalname, finalurl, current_page)
                return
            readURL()
            urls[finalname] = {'url': finalurl, 'pages': num_of_pages.get()}
            for value, key in urls.items():
                if key['url'] == finalurl:
                    key['pages'] = num_of_pages.get()
            writeURL()
            frame.destroy()
            driver.get(finalurl)
            readanswers()
            recorded_answers[finalname] = {}
            writeanswers()
            if len(driver.find_elements_by_class_name(
                    'freebirdFormviewerComponentsQuestionBaseTitle')) == 0 or driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent"):
                try:
                    driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent")[-1].click()
                except:
                    pass
                login_window(root, driver, finalname, finalurl, current_page)
            else:
                formanswer(root, driver, finalname, finalurl, current_page)

        num_of_pages = IntVar()
        pageflag = BooleanVar()
        num_of_pages.set(1)
        pageflag.set(False)
        formpage = LabelFrame(frame,
                              labelwidget=Checkbutton(frame, font=midfont, text='Form has more than one page',
                                                      variable=pageflag, command=lambda: changestate()))
        pageinput = Entry(formpage, font=midfont, width=10, textvariable=num_of_pages, state=DISABLED)

        for i in range(5):
            Label(frame, text='').pack()
        pageinput.pack(padx=2, pady=2)
        formpage.pack(padx=2, pady=2)
        for i in range(2):
            Label(frame, text='').pack()
        Button(frame, font=midfont, text='Confirm and Proceed', command=lambda: confirm()).pack()

    def addURL(name):
        url_input_variable = StringVar()

        def checkurl():
            check_url = url_input_variable.get()
            if 'docs.google.com' in check_url:
                driver.get(check_url)
                error.set('URL saved')
                addurl_frame.destroy()
                Label(frame, font=midfont, fg='green', text='URL: ' + check_url[:80] + '...').pack()
                howmanypages(check_url, name)
            else:
                url_input_variable.set('')
                error.set('Invalid URL')
                return

        addurl_frame = LabelFrame(frame, font=midfont, text='Type your URL')
        url_input = Entry(addurl_frame, width=80, font=midfont, textvariable=url_input_variable)
        url_input.pack(side=TOP, anchor=NW, padx=2, pady=2)
        addurl_frame.pack()
        Button(addurl_frame, font=midfont, text='Confirm', command=lambda: checkurl()).pack(side=BOTTOM, anchor=E)

    def addName(finalurl):
        name_input_variable = StringVar()
        addnameflag = BooleanVar()
        addnameflag.set(True)

        def changenamestate():
            if addnameflag.get():
                name_input.configure(state=NORMAL)
            else:
                name_input.configure(state=DISABLED)
                name_input_variable.set('')

        def checkname():
            name = name_input_variable.get()
            if str(name_input['state']) == 'disabled':
                addname_frame.destroy()
                Label(frame, font=midfont, fg='red', text='RECORD UNAVAILABLE').pack()
                howmanypages(finalurl, finalname='tmp')
            elif str(name_input['state']) == 'normal' and name != '':
                driver.get(finalurl)
                addname_frame.destroy()
                Label(frame, font=midfont, fg='green', text='Name: ' + name).pack()
                howmanypages(finalurl, name)
            else:
                name_input_variable.set('')
                error.set('Empty name')

        addname_frame = LabelFrame(frame, labelwidget=Checkbutton(frame, font=midfont, text='Type your name', variable=addnameflag, command=lambda: changenamestate()))
        Label(addname_frame, font=midfont, fg='orange',
              text="Auto-filling is unavailable for URL without a nickname.").pack()
        name_input = Entry(addname_frame, font=midfont, width=20, textvariable=name_input_variable)
        name_input.pack()
        Button(addname_frame, font=midfont, text='Confirm', command=lambda: checkname()).pack(side=BOTTOM, anchor=E)
        addname_frame.pack()

    def add_or_choose(tmpurl, namelist):
        def chosename(name):
            readURL()
            identical_name = False
            for each in urls:
                if each == name:
                    identical_name = True
                    break
            if name != '' and identical_name:
                choosename_frame.destroy()
                Label(frame,fg='green',font=midfont,text=f"Chosen name: {name}").pack()

                def manual_submit():
                    frame.destroy()
                    readanswers()
                    recorded_answers[name] = {}
                    writeanswers()
                    if len(driver.find_elements_by_class_name(
                            'freebirdFormviewerComponentsQuestionBaseTitle')) == 0 or driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent"):
                        try:
                            driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent")[-1].click()
                        except:
                            pass
                        login_window(root, driver, name, tmpurl, current_page)
                    else:
                        formanswer(root, driver, name, tmpurl, current_page)

                def auto_submit():
                    frame.destroy()
                    auto(root, driver, name)
                auto_manual_frame = LabelFrame(frame, font=midfont, text='Name found')
                Button(auto_manual_frame, font=midfont, text='Refill', command=lambda: manual_submit()).pack(side=RIGHT, padx=2, pady=2)
                Button(auto_manual_frame, font=midfont, text='Autofill', command=lambda: auto_submit()).pack(side=RIGHT, padx=2, pady=2)
                auto_manual_frame.pack()
            else:
                error.set('Empty Input or Name not in the list')

        def add_another_name(name):
            if name =='tmp':
                error.set('tmp is not a valid name. Name anything else.')
                return
            if name != '':
                choosename_frame.destroy()
                Label(frame, font=midfont, fg='green', text='Name: ' + name).pack()
                howmanypages(tmpurl, name)
            else:
                error.set('Empty Input')

        name_input_variable = StringVar()
        choosename_frame = LabelFrame(frame, font=midfont, text="Type one of the nickname(s) or add one.")
        bottom_frame = Frame(choosename_frame)
        Label(choosename_frame, font=midfont, text=namelist).pack()
        Entry(choosename_frame, font=midfont, width=20, textvariable=name_input_variable).pack()
        Button(bottom_frame, font=midfont, text="Choose", command=lambda: chosename(name_input_variable.get())).pack(side=RIGHT, padx=2, pady=3)
        Button(bottom_frame, font=midfont, text="Add/Reset Name", command=lambda: add_another_name(name_input_variable.get())).pack(side=RIGHT, padx=2, pady=3)
        Button(bottom_frame, font=midfont, text='Fill without Saving', command=lambda: howmanypages(tmpurl, finalname='tmp')).pack(side=RIGHT, padx=2, pady=3)
        bottom_frame.pack(side=BOTTOM, fill=X, expand=False)
        choosename_frame.pack()

    def firststep_submit():
        readRecord()
        if (not nickname.get() and not url.get()) or (nickname.get() and url.get() and ('docs.google.com' not in url.get())):
            error.set('Invalid URL or Empty Input')
            nickname.set('')
            url.set('')
            return
        if nickname.get()=='tmp':
            error.set('tmp is not a valid name. Name anything else.')
            nickname.set('')
            return
        if nickname.get() and url.get():
            nameorlink.destroy()
            nameorlink.destroy()
            Label(frame, font=midfont, fg='green', text='Name: ' + nickname.get()).pack()
            Label(frame, font=midfont, fg='green', text='URL: ' + url.get()[:80] + '...').pack()
            howmanypages(url.get(), nickname.get())
        elif nickname.get():
            readURL()
            tmpname = nickname.get()
            addQ = True
            for each in urls:
                if tmpname == each:
                    driver.get(urls[each]['url'])
                    addQ = False
            if addQ:
                readanswers()
                recorded_answers[tmpname] = {}
                writeanswers()
                nameorlink.destroy()
                Label(frame, font=midfont, fg='green', text='Name: ' + tmpname).pack()
                if addQ:
                    addURL(tmpname)
            else:
                def manual_submit():
                    frame.destroy()
                    readanswers()
                    recorded_answers[tmpname] = {}
                    writeanswers()
                    if len(driver.find_elements_by_class_name(
                            'freebirdFormviewerComponentsQuestionBaseTitle')) == 0 or driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent"):
                        try:
                            driver.find_elements_by_class_name("quantumWizButtonPaperbuttonContent")[-1].click()
                        except:
                            pass
                        login_window(root, driver, tmpname, urls[tmpname]['url'], current_page)
                    else:
                        formanswer(root, driver, tmpname, urls[tmpname]['url'], current_page)

                def auto_submit():
                    frame.destroy()
                    auto(root, driver, tmpname)
                auto_manual_frame = LabelFrame(frame,font=midfont,text='Name found')
                Button(auto_manual_frame,font=midfont,text='Refill',command=lambda :manual_submit()).pack(side=RIGHT,padx=2,pady=2)
                Button(auto_manual_frame,font=midfont,text='Autofill',command=lambda :auto_submit()).pack(side=RIGHT,padx=2,pady=2)
                auto_manual_frame.pack()
        else:
            readURL()
            check_url = url.get()
            addQ = True
            recorded_names = []
            try:
                driver.get(check_url)
            except:
                error.set('Invalid URL')
                url.set('')
                return
            for each in urls:
                if check_url == urls[each]['url']:
                    recorded_names.append(each)
                    driver.get(check_url)
                    addQ = False
            nameorlink.destroy()
            Label(frame, font=midfont, fg='green', text='URL: ' + check_url[:80] + '...').pack()
            if addQ:
                addName(check_url)
            else:
                add_or_choose(check_url, recorded_names)

    def redo():
        frame.destroy()
        driver.close()
        main(root, driver)

    option = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    option.add_argument(f'user-agent={user_agent}')
    option.add_argument("-incognito")
    option.add_argument("-headless")
    driver = webdriver.Chrome(chromedriverLocation['location'], options=option)
    Button(frame, font=midfont, text='Redo', command=lambda: redo()).pack(side=BOTTOM)
    Label(frame, font=midfont, text='').pack()
    nameorlinkbtn = Button(nameorlink, font=midfont, text="Confirm", command=lambda: firststep_submit())
    nameorlinkbtn.pack(side=BOTTOM, anchor=E)


def chromedriver_session(root):
    root.title("Chromedriver Setup")
    root.wm_geometry("700x200")
    frame = Frame(bd=4, relief=SUNKEN)
    frame.pack(side=BOTTOM, fill=BOTH, expand=True)
    error = StringVar()
    location = StringVar()
    Label(frame, font=midfont, fg='red', textvariable=error).pack(side=BOTTOM, anchor=W)
    readChrome()
    option = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    option.add_argument(f'user-agent={user_agent}')
    option.add_argument("-incognito")
    option.add_argument("-headless")
    def record_location(location_save):
        chromedriverLocation['location'] = location_save
        try:
            driver = webdriver.Chrome(chromedriverLocation['location'], options=option)
            writeChrome()
            frame.destroy()
            main(root, driver)
        except:
            location.set('')
            error.set('Invalid location')
            return

    try:
        driver = webdriver.Chrome(chromedriverLocation['location'], options=option)
        frame.destroy()
        main(root, driver)
    except:
        Label(frame, font=bigfont, text="Chromedriver location not found.\nYour chromedriver location:\n").pack()
        Entry(frame, font=midfont, width=70, textvariable=location).pack()
        Label(frame, font=midfont, text='').pack()
        Button(frame, font=midfont, text='Confirm', command=lambda: record_location(location.get())).pack()


def start():
    root = Tk()
    root.resizable(False, True)
    root.resizable(0, 0)
    chromedriver_session(root)
    root.mainloop()


bigfont = ('', 15)
midfont = ('', 12)
smallfont = ('', 10)
start()
