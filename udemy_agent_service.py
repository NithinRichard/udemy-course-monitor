#!/usr/bin/env python3
"""
Udemy Agent Windows Service Wrapper

This script provides Windows service functionality for the Udemy agent.
It can be registered as a Windows service to run automatically in the background.

Usage:
    python udemy_agent_service.py install    # Install as Windows service
    python udemy_agent_service.py start      # Start the service
    python udemy_agent_service.py stop       # Stop the service
    python udemy_agent_service.py remove     # Remove the service
"""

import sys
import os
import time
import logging
from pathlib import Path
import servicemanager
import win32serviceutil
import win32service
import win32event
import win32api
from udemy_agent_production import ProductionUdemyAgent

class UdemyAgentService(win32serviceutil.ServiceFramework):
    """Windows service wrapper for Udemy agent"""

    _svc_name_ = "UdemyCourseMonitor"
    _svc_display_name_ = "Udemy Free Course Monitor"
    _svc_description_ = "Monitors Udemy for free programming courses and sends email notifications"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.agent = None
        self.running = True

        # Setup service logging
        self.setup_service_logging()

    def setup_service_logging(self):
        """Setup logging for Windows service"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger('UdemyAgentService')
        self.logger.setLevel(logging.INFO)

        # Remove any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # File handler
        log_file = log_dir / "udemy_agent_service.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.info("Udemy Agent Service initialized")

    def SvcStop(self):
        """Called when the service is stopped"""
        self.logger.info("Service stop signal received")
        self.running = False

        if self.agent:
            self.agent.stop()

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """Main service function"""
        try:
            self.logger.info("Udemy Agent Service starting...")

            # Initialize the agent
            self.agent = ProductionUdemyAgent()

            # Run the agent
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )

            self.logger.info("Service started successfully")

            # Keep the service running
            while self.running:
                # The agent runs its own scheduler, so we just need to keep the service alive
                time.sleep(10)

                # Check if agent is still healthy
                if self.agent and hasattr(self.agent, 'health_status'):
                    status = self.agent.health_status.get('status', 'unknown')
                    if status == 'error':
                        self.logger.warning("Agent health status is ERROR, attempting recovery...")
                        # The production agent has its own recovery mechanisms

        except Exception as e:
            self.logger.error(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"Udemy Agent Service error: {e}")

        self.logger.info("Udemy Agent Service stopped")

def main():
    """Main entry point for service management"""

    if len(sys.argv) == 1:
        # Run as service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(UdemyAgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Handle service commands
        win32serviceutil.HandleCommandLine(UdemyAgentService)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Service management commands
        command = sys.argv[1].lower()

        if command in ['install', 'remove', 'start', 'stop', 'restart']:
            print(f"Executing command: {command}")

            if command == 'install':
                # Install service
                win32serviceutil.InstallService(
                    UdemyAgentService.__module__,
                    UdemyAgentService._svc_name_,
                    UdemyAgentService._svc_display_name_,
                    startType=win32service.SERVICE_AUTO_START
                )
                print("Service installed successfully")
                print("The service will start automatically on boot")
                print("To start manually: python udemy_agent_service.py start")

            elif command == 'remove':
                win32serviceutil.RemoveService(UdemyAgentService._svc_name_)
                print("Service removed successfully")

            elif command == 'start':
                win32serviceutil.StartService(UdemyAgentService._svc_name_)
                print("Service started successfully")

            elif command == 'stop':
                win32serviceutil.StopService(UdemyAgentService._svc_name_)
                print("Service stopped successfully")

            elif command == 'restart':
                win32serviceutil.RestartService(UdemyAgentService._svc_name_)
                print("Service restarted successfully")

        else:
            print("Usage:")
            print("  python udemy_agent_service.py install    # Install service")
            print("  python udemy_agent_service.py start      # Start service")
            print("  python udemy_agent_service.py stop       # Stop service")
            print("  python udemy_agent_service.py restart    # Restart service")
            print("  python udemy_agent_service.py remove     # Remove service")
    else:
        print("Udemy Agent Service")
        print("===================")
        print()
        print("This script should be run with service management commands:")
        print("  python udemy_agent_service.py install")
        print("  python udemy_agent_service.py start")
        print("  python udemy_agent_service.py stop")
        print("  python udemy_agent_service.py remove")
        print()
        print("Or run directly as a service (requires administrative privileges)")
        print()
        print("For more information, see README.md")