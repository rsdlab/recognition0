#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file recognition0.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import pygame
import speech_recognition as sr



recognizer = sr.Recognizer()
audio = None

directory = "/home/rsdlab/workspace/recognition0/voice/"
directory = "/home/rsdlab/workspace/health_judge/rtc/recognition0/voice/"
start_sound = directory + "kaishi.mp3"
stop_sound = directory + "shuryo.mp3"
# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
recognition0_spec = ["implementation_id", "recognition0", 
         "type_name",         "recognition0", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.judge", "false",
         "conf.default.inputtype", "voice",

         "conf.__widget__.judge", "text",
         "conf.__widget__.inputtype", "text",

         "conf.__type__.judge", "string",
         "conf.__type__.inputtype", "string",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class recognition0
# @brief ModuleDescription
# 
# 
# </rtc-template>
class recognition0(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_command_in = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
        """
        """
        self._command_inIn = OpenRTM_aist.InPort("command_in", self._d_command_in)
        self._d_text = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._textOut = OpenRTM_aist.OutPort("text", self._d_text)
        self._d_command_out = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._command_outOut = OpenRTM_aist.OutPort("command_out", self._d_command_out)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        
         - Name:  judge
         - DefaultValue: false
        """
        self._judge = ['false']
        """
        
         - Name:  inputtype
         - DefaultValue: voice
        """
        self._inputtype = ['voice']
		
        # </rtc-template>


    def onInitialize(self):
        # Bind variables and configuration variable
        self.bindParameter("judge", self._judge, "false")
        self.bindParameter("inputtype", self._inputtype, "voice")

        # Set InPort buffers
        self.addInPort("command_in",self._command_inIn)
		
        # Set OutPort buffers
        self.addOutPort("text",self._textOut)
        self.addOutPort("command_out",self._command_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK


    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	

    def onDeactivated(self, ec_id):
    
        return RTC.RTC_OK
	

    def onExecute(self, ec_id):

        try:
            if self._command_inIn.isNew(): 
                command = self._command_inIn.read()
                print(f"コマンド {command.data}")

                if command.data[1] == 10:
                    languages = "ja-JP"

                elif command.data[1]  == 11:
                    languages = "en-US"

                elif command.data[1]  == 12:
                    languages = "fr-FR"

                else:
                    print("no")


                print(self._inputtype[0])
                recognized_text = recognize(self._inputtype[0], command.data[0], languages)
                print(f"返答: {recognized_text}")

                self._d_command_out.data = recognized_text
                self._d_text.data = recognized_text
                print(self._d_text.data)

                self._command_outOut.write()
                self._textOut.write()
        except Exception as e:
            print(e)

        return RTC.RTC_OK
	


def recognize(inputtype, state, languages):
    retry_limit = 2
    attempts = 0

    if inputtype == 'voice':
        # #print("入力してください")
        # recognized_text = input()
        # return recognized_text
        while attempts < retry_limit:
            if state == 1:
                print(state)
                print("音声認識は停止中です。")
                break
            try:
                with sr.Microphone() as source:
                    print("Adjusting for ambient noise.")
                    recognizer.adjust_for_ambient_noise(source)  # 周囲のノイズを調整
                    print("話しかけてください...")
                    
                    pygame.mixer.init()
                    pygame.mixer.music.load(start_sound)
                    
                    pygame.mixer.music.play()

                    audio = recognizer.listen(source,phrase_time_limit=5)  # 音声をキャプチャ

                    pygame.mixer.init()
                    pygame.mixer.music.load(stop_sound)
                    pygame.mixer.music.play()
                
                time.sleep(0.5)
                
                text = '>> 音声認識しています...'
                print('\r' + '　' * 40 + '\r', end='', flush=True)
                print(text)
                recognized_text = recognizer.recognize_google(audio, language=languages)  # 日本語認識

                
                print(f"認識された内容: {recognized_text}")

                # 認識に成功したら、テキストを返して終了
                return recognized_text

            except sr.UnknownValueError:
                text = "上手く聞き取れませんでした．もう一度お願いします"
                print('\r' + '　' * 40 + '\r', end='', flush=True)
            
            except sr.RequestError as e:
                text = "結果をリクエストできませんでした.\n"
                print('\b' * 20, end='', flush=True)
                print('　' * 20 + '\n', end='', flush=True)
                print(f"結果をリクエストできませんでした．; {e}")
                result = "ERROR" 
                return result

            except Exception as e:
                print(f"予期しないエラーが発生しました: {e}")
                result = "ERROR" 
                return result

            attempts += 1
            print(f"再試行回数: {attempts}/{retry_limit}")

        if state != 1:
            print("リトライの上限に達しました。認識に失敗しました。")

        # リトライ上限に達した場合は None を返す
        return "ERROR"  

    else:
        print("入力してください")
        recognized_text = input()
        return recognized_text

def recognition0Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=recognition0_spec)
    manager.registerFactory(profile,
                            recognition0,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    recognition0Init(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("recognition0" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

