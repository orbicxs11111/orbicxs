import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QStatusBar, QTabWidget, QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orbicxs Browser")
        self.setGeometry(100, 100, 1280, 800)

        # Tablar
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Birinchi tab
        self.add_new_tab(QUrl("https://orbicxs.com"), "Orbicxs")

        # Toolbar
        self.create_toolbar()

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        back_btn = QAction("← Back", self)
        back_btn.setShortcut(QKeySequence("Back"))
        back_btn.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(back_btn)

        forward_btn = QAction("→ Forward", self)
        forward_btn.setShortcut(QKeySequence("Forward"))
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(forward_btn)

        reload_btn = QAction("↻ Reload", self)
        reload_btn.setShortcut(QKeySequence("Refresh"))
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(reload_btn)

        home_btn = QAction("🏠 Home", self)
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setMinimumWidth(500)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        # New Tab
        new_tab_btn = QAction("+ New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl("https://google.com"), "New Tab"))
        toolbar.addAction(new_tab_btn)

    def add_new_tab(self, qurl=QUrl("https://orbicxs.com"), label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))
        
        browser.loadFinished.connect(lambda: self.tabs.setTabText(
            self.tabs.currentIndex(), 
            browser.page().title()[:30] or label
        ))

        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        if text.startswith(("http://", "https://")):
            self.current_browser().setUrl(QUrl(text))
            return

        if "." in text and " " not in text:
            if not text.startswith("www."):
                text = "www." + text
            self.current_browser().setUrl(QUrl("https://" + text))
            return

        # Google qidiruvi
        search_url = f"https://www.google.com/search?q={text.replace(' ', '+')}"
        self.current_browser().setUrl(QUrl(search_url))

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://orbicxs.com"))

    def update_url_bar(self, qurl, browser=None):
        if browser == self.current_browser():
            self.url_bar.setText(qurl.toString())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(0xAA, True)   # High DPI support
    window = Browser()
    window.show()
    sys.exit(app.exec_())
