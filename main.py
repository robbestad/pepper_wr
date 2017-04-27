#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import sys
import qi
import argparse
import os


class AcandoWebRebels(object):
    def __init__(self, application):
        # Getting a session that will be reused everywhere
        self.application = application
        self.session = application.session
        self.service_name = self.__class__.__name__

        # Getting a logger. Logs will be in /var/log/naoqi/servicemanager/{application id}.{service name}
        self.logger = qi.Logger(self.service_name)

        # Do some initializations before the service is registered to NAOqi
        self.logger.info("Initializing...")

        self.tts = self.session.service("ALTextToSpeech")
        self.memory = self.session.service("ALMemory")
        self.system = self.session.service("ALSystem")
        self.memory.insertData("EnemiesOfTheAvenger", 1)

        self.dialog = self.session.service("ALDialog")
        self.dialog.setLanguage("English")

        topic_path = os.path.realpath(os.path.join(os.getcwd(), "dialog", "topic1.top"))
        self.first_topic = self.dialog.loadTopic(topic_path.encode('utf-8'))

        # Activating the loaded topic
        self.dialog.activateTopic(self.first_topic)

        # Starting the dialog engine - we need to type an arbitrary string as the identifier
        # We subscribe only ONCE, regardless of the number of topics we have activated
        self.dialog.subscribe('acando_dialogs')

        # Getting a logger. Logs will be in /var/log/naoqi/servicemanager/{application id}.{service name}
        self.logger = qi.Logger(self.service_name)

        # @TODO: insert init functions here
        self.logger.info("Initialized!")

    @qi.nobind
    def start_app(self):
        # do something when the service starts
        self.logger.info("Starting...")

        try:
            robotName = self.system.robotName()
            # robotName = "the avenger"
            self.tts.say("\\rspd=45\\ " + robotName + " at your service")
            #exit(0)

        except RuntimeError, e:
            print "i fail"
            print str(e)
            exit(1)

        # @TODO: insert whatever the app should do to start
        self.logger.info("Started!")

    @qi.nobind
    def stop_app(self):
        # To be used if internal methods need to stop the service from inside.
        # external NAOqi scripts should use ALServiceManager.stopService if they need to stop it.
        self.logger.info("Stopping service...")
        self.application.stop()
        self.logger.info("Stopped!")

    @qi.nobind
    def cleanup(self):
        # called when your module is stopped
        self.logger.info("Cleaning...")
        self.dialog.deactivateTopic(self.first_topic)
        self.dialog.unsubscribe('acando_dialogs')

        # @TODO: insert cleaning functions here
        self.logger.info("Cleaned!")


if __name__ == "__main__":
    # with this you can run the script for tests on remote robots
    # run : python main.py --qi-url 123.123.123.123
    app = qi.Application(sys.argv)
    app.start()
    service_instance = AcandoWebRebels(app)
    service_id = app.session.registerService(service_instance.service_name, service_instance)
    service_instance.start_app()
    app.run()
    service_instance.cleanup()
    app.session.unregisterService(service_id)
