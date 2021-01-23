# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException

import argparse

import time
import os
import re

class EmptyCredentials(Exception):
    pass

class Recorder():
    def recorder_control(self,start=''):
        pass
    def recorder_config(self):
        pass

class Uucps(Recorder):

    def __init__(self):
        self.dirname=os.path.dirname(__file__)
        self.pre_url='https://study.enaea.edu.cn'


    def check_box_and_exit(self):
        while True:
            time.sleep(1)
            '''20 mins check box'''
            container = self.driver.find_elements_by_class_name('dialog-button-container')
            if len(container) != 0:
                container[0].find_element_by_xpath('.//*').click()
                self.driver.fullscreen_window()

            ''' break if at the end of this course'''
            '''
            playing
                    style 'display: none; z-index: 1500;'
                    class 'ccH5PlayBtn'
            pause
                    style 'display: block; z-index: 1500;'
                    class 'ccH5PlayBtn'
            end
                    style 'display: block; z-index: 1500;'
                    class 'adrPlayBtn'
            '''
            replaybutton=self.driver.find_element_by_id('replaybtn')
            #if len(replaybutton) != 0:
            if 'adrPlayBtn' in replaybutton.get_attribute('class'):
                time.sleep(5)
                replaybutton=self.driver.find_element_by_id('replaybtn')
                if 'adrPlayBtn' in replaybutton.get_attribute('class'):
                    self.driver.close()
                    break
                else:
                    # this course next video
                    self.driver.fullscreen_window()

    def _recorder_control(self,start=''):
        '''control ssr start/stop'''
        if start=='start':
            command='simplescreenrecorder --settingsfile=%s/settings.conf < <(echo window-hide;echo record-start) >/dev/null 2>&1 &' % self.dirname
            #print(command)
            os.system(command)
        elif start == 'stop':
            os.system('killall -TERM simplescreenrecorder')


    def the_first_unlearned_button_in_this_page(self):
        '''recording: self.recording_subdir_name, self.recording_file_name'''

        course_table=self.driver.find_elements_by_class_name('dataTables_wrapper')
        table_body=course_table[0].find_elements_by_xpath('.//tbody')
        table_data=course_table[0].find_elements_by_xpath('.//tbody/*')

        table_hight=len(table_data)

        for index in range(1,table_hight):
            process = table_body[0].find_elements_by_xpath('.//tr['+str(index)+']/td[5]/div/p')

            if len(process) != 0:
                if process[0].text == '100%':
                    continue
                else:
                    # recorder
                    self.recording_file_name=table_body[0].find_element_by_xpath('.//tr[' +str(index)+ ']/*').text # lecture name
                    self.recording_file_name += '-'
                    self.recording_file_name += table_body[0].find_element_by_xpath('.//tr[' +str(index)+ ']/td[3]/*').text # teachers name
                    self.recording_file_name += '.mkv'

                    to_be_learned_button=table_body[0].find_elements_by_xpath('.//tr['+str(index)+']/td[6]/a')
                    self.now_to_learn_url=self.pre_url+str(to_be_learned_button[0].get_attribute('data-vurl'))
                    break
            else:
                self.recording_subdir_name=table_body[0].find_element_by_xpath('.//tr[' +str(index)+ ']/*').text

    def get_credentials(self):
        '''self.username self.password'''
        self.credentials=self.dirname+'/login.conf'

        with open(self.credentials) as f:
            credentials = f.readlines()
        if len(credentials) != 2:
            raise EmptyCredentials

        username=credentials[0].strip()
        password=credentials[1].strip()
        self.username=re.sub(r'^username=','',username,1)
        self.password=re.sub(r'^password=','',password,1)


    def _recorder_config(self):
        '''self.ssr_config'''
        self.recording_full_dir_name=self.recording_predir_name +'/'+ self.recording_subdir_name
        os.makedirs(self.recording_full_dir_name,exist_ok=True)

        self.recording_full_dir_file_name=self.recording_full_dir_name+'/'+self.recording_file_name
        encoded_recording_file=self.recording_full_dir_file_name.encode("unicode_escape").decode("utf-8").replace('\\u','\\x')

        self.ssr_config=self.dirname + '/settings.conf'
        with open(self.ssr_config_template) as fr:
            for line in fr:
                if line.startswith('file='):
                    line='file='+encoded_recording_file+'\n'
                with open(self.ssr_config,'a') as fw:
                    fw.write(line)

    def login(self):
        '''login page'''
        time.sleep(1)

        username=self.driver.find_elements_by_name('username')
        password=self.driver.find_elements_by_name('password')
        login_button=self.driver.find_elements_by_class_name('btn-row')
        for i in range(len(username)):
            try:
                username[i].send_keys(self.username)
                password[i].send_keys(self.password)
                break
            except ElementNotInteractableException:
                pass
        for i in range(len(login_button)):
            try:
                time.sleep(1)
                login_button[i].click()
                break
            except ElementNotInteractableException:
                pass
        time.sleep(2)

    def start_watching(self,ssr_config_template,main_dir_to_save_recordings):
        if ssr_config_template:
            self.ssr_config_template=os.path.abspath(os.path.expanduser(ssr_config_template))
        else:
            self.ssr_config_template=os.path.abspath(os.path.expanduser('~/.ssr/settings.conf'))

        try:
            self.recording_predir_name=os.path.abspath(os.path.expanduser(main_dir_to_save_recordings))
            self.recorder_config = self._recorder_config
            self.recorder_control = self._recorder_control
        except TypeError:
            # do not record
            pass

        try:
            self.get_credentials()
        except EmptyCredentials:
            print("""\n login.conf format:\n\n username=<username>\n password=<password>\n\n Do not add any empty Line.""")
            return


        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.pre_url+'/login.do')


        self.login()

        # 个人空间
        self.driver.execute_script('document.getElementsByClassName("button")[0].click();')
        time.sleep(2)
        # net tab 进入学习
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 必修课
        self.driver.execute_script('document.querySelector("#sideNav > ul > li:nth-child(3) > a").click();')
        time.sleep(2)


        while True:
            '''Change pages until find not learned course.'''
            #course_list=self.driver.find_elements_by_class_name('progressvalue')
            # get the unlearned courses
            self.the_first_unlearned_button_in_this_page()

            while not self.now_to_learn_url: # click next_page until found
                finished=1
                nextpage_button=self.driver.find_element_by_id('J_myOptionRecords_next')
                if not ('disabled' in nextpage_button.get_attribute('class')): # not find and there is next page
                    nextpage_button.click()
                    time.sleep(2)
                else:
                    finished=1
                self.the_first_unlearned_button_in_this_page()
                if finished:
                    break
            '''none'''


            self.driver.execute_script('window.open("' +self.now_to_learn_url+ '","_blank");' )
            #self.driver.get(learn_url)
            time.sleep(2)

            # new_tab 上课界面
            window_name=self.driver.window_handles[2]
            self.driver.switch_to.window(window_name=window_name)
            time.sleep(2)

            self.recorder_config()

            self.driver.fullscreen_window()

            try:
                self.recorder_control('start')
                self.driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)

                self.check_box_and_exit()
                self.recorder_control('stop')
            except:
                os.system('killall -TERM simplescreenrecorder')

            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.refresh()
            time.sleep(2)

        self.driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='大学生网络党校课程自动录屏')
    parser.add_argument('-c', '--ssr-config', help='simplescreenrecorder 配置模板文件，默认~/.ssr/settings.conf')
    parser.add_argument('-o', '--save-recording-path', help='若要录屏，录屏文件夹位置')
    args = parser.parse_args()

    uucps=Uucps()
    uucps.start_watching(args.ssr_config,args.save_recording_path)
