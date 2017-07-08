
// KCrawlerControalDlg.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCrawlerControalDlg.h"
#include "afxdialogex.h"
#include "CreateJobDlg.h"
#include "KCCPlugins.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// ����Ӧ�ó��򡰹��ڡ��˵���� CAboutDlg �Ի���

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

// ʵ��
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CKCCDlg �Ի���



CKCCDlg::CKCCDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_KCRAWLERCONTROAL_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CKCCDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_EDIT_LOG, m_edit_log);
	DDX_Control(pDX, IDC_LIST_CRAWLERLIST, m_liat_crawlerlist);
}

BEGIN_MESSAGE_MAP(CKCCDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON_CREATEJOB, &CKCCDlg::OnBnClickedButtonCreatejob)
	ON_MESSAGE(WM_UPDATE_CRAWLER_LIST,onLoadCrawlerList)
	ON_MESSAGE(WM_DOWNLOAD_RESULT,onDownloadResultMsg)
	ON_BN_CLICKED(IDC_BUTTON_DOWNLOAD_RESULT_FILE, &CKCCDlg::OnBnClickedButtonDownloadResultFile)
	ON_BN_CLICKED(IDC_BUTTON_LOADANALY, &CKCCDlg::OnBnClickedButtonLoadanaly)
END_MESSAGE_MAP()


// CKCCDlg ��Ϣ�������

BOOL CKCCDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// ��������...���˵�����ӵ�ϵͳ�˵��С�

	// IDM_ABOUTBOX ������ϵͳ���Χ�ڡ�
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// ���ô˶Ի����ͼ�ꡣ  ��Ӧ�ó��������ڲ��ǶԻ���ʱ����ܽ��Զ�
	//  ִ�д˲���
	SetIcon(m_hIcon, TRUE);			// ���ô�ͼ��
	SetIcon(m_hIcon, FALSE);		// ����Сͼ��

	AfxSocketInit();
	firstrun = true;
	// TODO: �ڴ���Ӷ���ĳ�ʼ������
	loadConfig();
	InitEnvirment();
	LoadCrawlerList();
	//ѭ�����������б�
	AfxBeginThread(LoopLoadCrawlerList, AfxGetMainWnd()->m_hWnd);

	return TRUE;  // ���ǽ��������õ��ؼ������򷵻� TRUE
}

int CKCCDlg::DATA_REFRESH_RATE = 5;

void CKCCDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// �����Ի��������С����ť������Ҫ����Ĵ���
//  �����Ƹ�ͼ�ꡣ  ����ʹ���ĵ�/��ͼģ�͵� MFC Ӧ�ó���
//  �⽫�ɿ���Զ���ɡ�

void CKCCDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // ���ڻ��Ƶ��豸������

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// ʹͼ���ڹ����������о���
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// ����ͼ��
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//���û��϶���С������ʱϵͳ���ô˺���ȡ�ù��
//��ʾ��
HCURSOR CKCCDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CKCCDlg::OnBnClickedButtonCreatejob()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	CCreateJobDlg CCD;
	JobCreateData JCD;
	CCD.tiebaName = _T("�ɶ���Ϣ���̴�ѧ");
	CCD.pages = 0;
	CCD.DoModal();
	JCD.tiebaName = CCD.tiebaName;
	JCD.pages = CCD.pages;
	if (!KCCCreateJob(JCD))
	{
		KCCLog(_T(">>>>>���񴴽�ʧ�ܣ�\n"));
	}
	else
	{
		KCCLog(_T(">>>>>���񴴽��ɹ���\n"));
	}
}

LRESULT  CKCCDlg::onLoadCrawlerList(WPARAM WP, LPARAM LP)
{
	if (DEBUG_MODE)
	{
		return 0;
	}
	LoadCrawlerList();
	return 0;
}

LRESULT CKCCDlg::onDownloadResultMsg(WPARAM WP, LPARAM LP)
{
	CSocket s;
	s.Socket();
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("�����޷����ӵ�TaskManager����������������������Ӻ����ԣ�"));
		return 0;
	}
	KCCLog(_T("������..."));
	CString RESULT_TRANSFER_CMD = _T("304,REQUEST FOR JOB RESULT");
	USES_CONVERSION;
	char *cmdbuf = T2A(RESULT_TRANSFER_CMD);
	cmdbuf = UnicodeToUTF8(RESULT_TRANSFER_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	KCCLog(_T("�����ѷ��ͣ��ȴ�TaskManager��������Ӧ..."));
	CString cp;
	char recvBuf[1024] = { 0 };
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));
	//��ʼ�����ļ�
	//���ȵõ��ļ���С
	memset(recvBuf, 0, sizeof(char) * 1024);
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:->result file size:" + cp));
	int filesize = _ttoi(cp);
	//Ȼ��ʼ����
	CString filedata = _T("");
	int recivedsize = 0;
	KCCLog(_T("������...."));
	CFile re;
	re.Open(_T("result"), CFile::modeCreate | CFile::modeWrite | CFile::typeBinary);
	while (recivedsize < filesize)
	{
		memset(recvBuf, 0, sizeof(char) * 1024);
		int rs = s.Receive((void *)recvBuf, 1024);
		re.Write(recvBuf,rs);
		cp = UTF8_TO_GBK(recvBuf);
		filedata += cp;
		recivedsize += rs;
	}
	KCCLog(_T("������������ϣ�"));
	s.Close();
	re.Close();
	return 0;
}

void CKCCDlg::loadConfig()
{
	CStdioFile cfg;
	cfg.Open(PATH_CONFIG_FILE,CFile::modeRead);
	CString line = _T("");
	while (cfg.ReadString(line))
	{
		//MessageBox(line);
		if(line.Find(_T("SERVER_HOST")) >= 0){
			//��ȡ��������ַ
			DATA_SERVER_IP = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
		}
		else if(line.Find(_T("SERVER_PORT")) >= 0) {
			//��ȡ�˿�
			DATA_SERVER_PORT = _ttoi(line.Right(line.GetLength() - line.Find(_T("=")) - 1));
			if (DATA_SERVER_PORT > 65536)
			{
				DATA_SERVER_PORT = 50005;
			}
		}
		else if(line.Find(_T("REFRESH_RATE")) >= 0) {
			//��ȡ���������б�Ƶ��
			DATA_REFRESH_RATE = _ttoi(line.Right(line.GetLength() - line.Find(_T("=")) - 1));
			if (DATA_REFRESH_RATE < 3)
			{
				DATA_REFRESH_RATE = 5;
			}
		}
		else if(line.Find(_T("MODE_DEBUG")) >= 0) {
			//�Ƿ�������ģʽ
			if (line.Right(line.GetLength() - line.Find(_T("=")) - 1) == _T("TRUE"))
			{
				DEBUG_MODE = true;
			}
		}
		line = _T("");
	}
	cfg.Close();
}


void CKCCDlg::KCCLog(const CString logdata)
{
	m_edit_log.SetSel(m_edit_log.GetSel());
	m_edit_log.ReplaceSel(_T(">>>>>"+ logdata +"\n"));
	m_edit_log.LineScroll(m_edit_log.GetLineCount());
}

const bool CKCCDlg::KCCCreateJob(const JobCreateData jcd)
{
	KCCLog(_T("��ʼ��..."));
	CSocket s;
	s.Socket();
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("�����޷����ӵ�TaskManager����������������������Ӻ����ԣ�"));
		return false;
	}
	KCCLog(_T("���������嵥..."));
	CString JOB_CREATE_CMD = _T("303,TEST,");
	CString cp;
	//һ�������嵥����
	cp.Format(_T("%d"), jcd.pages);
	JOB_CREATE_CMD += (jcd.tiebaName + _T(",") + cp);
	USES_CONVERSION;
	char *cmdbuf = T2A(JOB_CREATE_CMD);
	cmdbuf = UnicodeToUTF8(JOB_CREATE_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	KCCLog(_T("�����嵥������ϣ��ȴ�TaskManager��������Ӧ..."));
	char recvBuf[1024] = { 0 };
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));
	//����ȷ��
	JOB_CREATE_CMD = _T("666,JOB COMFIRM");
	KCCLog(_T("ȷ��������..."));
	cmdbuf = UnicodeToUTF8(JOB_CREATE_CMD.GetBuffer(0));
	s.Send(cmdbuf, strlen(cmdbuf));
	s.Receive((void *)recvBuf, 1024);
	cp = UTF8_TO_GBK(recvBuf);
	KCCLog(_T("TaskManager:" + cp));

	s.Close();
	return true;
}

void CKCCDlg::InitEnvirment()
{
	//��ʼ�������б�ؼ�
	//������ ����ID��IP��ַ���˿ڣ�����״̬������ʱ��
	int size[10] = { 50,220,80,80,120 };
	CString name[10] = { _T("ID") ,_T("IP��ַ") ,_T("�˿�") ,_T("����״̬") ,_T("����ʱ��") };
	for (int i = 0; i < 5; i++)
	{
		m_liat_crawlerlist.InsertColumn(i, (LPWSTR)(LPCTSTR)name[i], LVCFMT_CENTER, size[i]);
	}
	
}

void  CKCCDlg::LoadCrawlerList()
{
	CSocket s;
	s.Socket();
	char recvBuf[1024] = { 0 };
	if (firstrun)
	{
		KCCLog(_T("���������б�..."));
	}
	if (!s.Connect(DATA_SERVER_IP, DATA_SERVER_PORT))
	{
		KCCLog(_T("�����޷�ˢ�������б�->�޷����ӵ�TaskManager������->��������������Ӻ����ԣ�"));
		return ;
	}
	//ȥ���������Ļ�ӭ��Ϣ
	s.Receive((void *)recvBuf, 1024);
	CString REQUEST_CRAWLER_LIST = _T("302,request for crawler list");
	CString cp;
	USES_CONVERSION;
	//��������
	char *cmdbuf = T2A(REQUEST_CRAWLER_LIST);
	s.Send(cmdbuf, strlen(cmdbuf));
	memset(recvBuf, 0, sizeof(char) * 1024);
	s.Receive(recvBuf, 1024);
	s.Close();
	cp = UTF8_TO_GBK(recvBuf);
	if (firstrun)
	{
		KCCLog(_T("TaskManager:" + cp));
		KCCLog(_T("�����б������ɣ�"));
	}
	//��ListControl�м��������б�
	cp = cp.Right(cp.GetLength() - cp.Find(',') - 1);
	cp = cp.Left(cp.Find(','));
	//MessageBox(cp);
	int lastat = 0;
	int online = 0;
	m_liat_crawlerlist.DeleteAllItems();
	while (cp.GetLength() > 0)
	{
		lastat = cp.Find('@');
		CString ID = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		CString IP = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		CString PORT = cp.Left(cp.Find('@'));
		cp = cp.Right(cp.GetLength() - cp.Find('@') - 1);
		//MessageBox(cp);
		if (ID == "" || ID == " ")
		{
			continue;
		}
		m_liat_crawlerlist.InsertItem(online,ID);
		m_liat_crawlerlist.SetItemText(online, 1, IP);
		m_liat_crawlerlist.SetItemText(online, 2, PORT);
		m_liat_crawlerlist.SetItemText(online, 3, _T("N/A"));
		m_liat_crawlerlist.SetItemText(online, 4, _T("N/A"));
		online++;
		if (cp.Find('@') < 0)
		{
			break;
		}
	}
	cp.Format(_T("%d"), online);
	SetDlgItemText(IDC_STATIC_CRAWLERSUM, cp);
	firstrun = false;
}

UINT  CKCCDlg::LoopLoadCrawlerList(LPVOID pParam)
{
	HWND TH = (HWND)pParam;
	if (TH == nullptr)
	{
		return -1;  //-1 = ��ָ��
	}
 	while (true)
	{
		Sleep(1000*DATA_REFRESH_RATE);
		::PostMessage(TH,WM_UPDATE_CRAWLER_LIST,NULL,NULL);
	}
	return 0;
}

UINT  CKCCDlg::DownloadResultNewThread(LPVOID pParam)
{
	HWND TH = (HWND)pParam;
	if (TH == nullptr)
	{
		return -1;  //-1 = ��ָ��
	}
	::PostMessage(TH, WM_DOWNLOAD_RESULT, NULL, NULL);
	return 0;
}

const wchar_t*  CKCCDlg::UTF8_TO_GBK(const char* str)
{//
	int    textlen = 0;
	wchar_t * result;
	textlen = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
	result = (wchar_t *)malloc((textlen + 1) * sizeof(wchar_t));
	memset(result, 0, (textlen + 1) * sizeof(wchar_t));
	MultiByteToWideChar(CP_UTF8, 0, str, -1, (LPWSTR)result, textlen);
	return    result;
}

char * CKCCDlg::UnicodeToUTF8(const wchar_t *str)
{
	char * result;
	int textlen = 0;
	// wide char to multi char
	textlen = WideCharToMultiByte(CP_UTF8, 0, str, -1, NULL, 0, NULL, NULL);
	result = (char *)malloc((textlen + 1) * sizeof(char));
	memset(result, 0, sizeof(char) * (textlen + 1));
	WideCharToMultiByte(CP_UTF8, 0, str, -1, result, textlen, NULL, NULL);
	return result;
}


void CKCCDlg::OnBnClickedButtonDownloadResultFile()
{
	AfxBeginThread(DownloadResultNewThread, AfxGetMainWnd()->m_hWnd);
}


void CKCCDlg::OnBnClickedButtonLoadanaly()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	KCCPlugins kccp;
	kccp.DoModal();
}
