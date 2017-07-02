// KCrawlerControalDlg.h : ͷ�ļ�
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

// CKCCDlg �Ի���
class CKCCDlg : public CDialogEx
{
// ����
public:
	CKCCDlg(CWnd* pParent = NULL);	// ��׼���캯��

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_KCRAWLERCONTROAL_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV ֧��


// ʵ��
protected:
	HICON m_hIcon;

	// ���ɵ���Ϣӳ�亯��
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedButtonCreatejob();
	afx_msg LRESULT onLoadCrawlerList(WPARAM WP, LPARAM LP);  //��Ӧ�����б������Ϣ����
	afx_msg LRESULT onDownloadResultMsg(WPARAM WP, LPARAM LP);  //��Ӧ����ץȡ�������Ϣ

//�Լ���ӵĺ����ͱ���
public:
	//����
	CString PATH_CONFIG_FILE = _T("config.ini");
	//CString DATA_SERVER_IP = _T("216.45.55.153");
	CString DATA_SERVER_IP = _T("ec2-54-238-242-34.ap-northeast-1.compute.amazonaws.com");  //amazon ECS
	int DATA_SERVER_PORT = 50005;
	static int DATA_REFRESH_RATE;
	bool DEBUG_MODE = false;
	// ��־�༭�����
	CEdit m_edit_log;
	// �����б�ؼ�
	CListCtrl m_liat_crawlerlist;

	//����
	void loadConfig();	//���������ļ������ó�ʼֵ
	void KCCLog(const CString logdata);   //׷����־
	const bool KCCCreateJob(const JobCreateData jcd);  //��������
	void InitEnvirment(); //��ʼ����ػ���
	void  LoadCrawlerList(); //�ӷ������������������б�
	static UINT  LoopLoadCrawlerList(LPVOID pParam);  //�����߳���ѭ�����������б�
	static UINT  DownloadResultNewThread(LPVOID pParam); //�����߳������ؽ���ļ�
	//����ת������
	const wchar_t*  UTF8_TO_GBK(const char* str);
	char * UnicodeToUTF8(const wchar_t *str);

private:
	bool firstrun;
	
public:
	afx_msg void OnBnClickedButtonDownloadResultFile();
	afx_msg void OnBnClickedButtonLoadanaly();
};
