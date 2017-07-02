#pragma once
#include "afxwin.h"


// KCCPlugins �Ի���

struct Plugin {
	CString name;
	CString descri;
	CString exefilename;
};

class KCCPlugins : public CDialogEx
{
	DECLARE_DYNAMIC(KCCPlugins)

public:
	KCCPlugins(CWnd* pParent = NULL);   // ��׼���캯��
	virtual ~KCCPlugins();

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_USE_PLUGINS };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

	DECLARE_MESSAGE_MAP()

public:
	//Python������
	CString PATH_PLUGINS_INDEX_FILE = _T("plugins.list");
	Plugin *pluginlist;
	void loadPlugins();   //���ز��������������ť�������ť�¼���
	void setupBasicInfo();  //��������Ļ�����Ϣ
	CString SearchPlugs();   //�°������ã�ֱ������pluginĿ¼
	void LoadPluginsNV();  //�µļ��ز���ķ���
						  // ��ʾ�����Ϣ���б��ؼ�
	CComboBox m_pluginslist;
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedOnExcutePlugings();
};
