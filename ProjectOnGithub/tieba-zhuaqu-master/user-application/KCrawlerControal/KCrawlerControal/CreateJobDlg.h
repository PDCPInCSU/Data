#pragma once


// CCreateJobDlg �Ի���

class CCreateJobDlg : public CDialogEx
{
	DECLARE_DYNAMIC(CCreateJobDlg)

public:
	CCreateJobDlg(CWnd* pParent = NULL);   // ��׼���캯��
	virtual ~CCreateJobDlg();
	CString tiebaName;
	int pages;

// �Ի�������
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_DIALOG_CREATE_JOB };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV ֧��

	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnBnClickedOk();
};
