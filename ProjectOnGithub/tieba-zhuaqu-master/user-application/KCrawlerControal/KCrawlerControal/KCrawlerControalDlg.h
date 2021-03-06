// KCrawlerControalDlg.h : 头文件
//

#pragma once
#include "afxwin.h"
#include "afxcmn.h"

#define WM_UPDATE_CRAWLER_LIST WM_USER+100
#define WM_DOWNLOAD_RESULT WM_USER+200

struct JobCreateData {
	CString tiebaName;
	int pages;
};

// CKCCDlg 对话框
class CKCCDlg : public CDialogEx
{
// 构造
public:
	CKCCDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_KCRAWLERCONTROAL_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButtonCreatejob();
	afx_msg LRESULT onLoadCrawlerList(WPARAM WP, LPARAM LP);  //响应爬虫列表更新消息函数
	afx_msg LRESULT onDownloadResultMsg(WPARAM WP, LPARAM LP);  //响应下载抓取结果的消息

//自己添加的函数和变量
public:
	//变量
	CString PATH_CONFIG_FILE = _T("config.ini");
	//CString DATA_SERVER_IP = _T("216.45.55.153");
	CString DATA_SERVER_IP = _T("ec2-54-238-242-34.ap-northeast-1.compute.amazonaws.com");  //amazon ECS
	int DATA_SERVER_PORT = 50005;
	static int DATA_REFRESH_RATE;
	bool DEBUG_MODE = false;
	// 日志编辑框变量
	CEdit m_edit_log;
	// 爬虫列表控件
	CListCtrl m_liat_crawlerlist;

	//函数
	void loadConfig();	//加载配置文件并设置初始值
	void KCCLog(const CString logdata);   //追加日志
	const bool KCCCreateJob(const JobCreateData jcd);  //创建任务
	void InitEnvirment(); //初始化相关环境
	void  LoadCrawlerList(); //从服务器加载在线爬虫列表
	static UINT  LoopLoadCrawlerList(LPVOID pParam);  //在新线程中循环加载爬虫列表
	static UINT  DownloadResultNewThread(LPVOID pParam); //在新线程中下载结果文件
	//编码转换函数
	const wchar_t*  UTF8_TO_GBK(const char* str);
	char * UnicodeToUTF8(const wchar_t *str);

private:
	bool firstrun;
	
public:
	afx_msg void OnBnClickedButtonDownloadResultFile();
	afx_msg void OnBnClickedButtonLoadanaly();
};
