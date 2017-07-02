// CreateJobDlg.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "CreateJobDlg.h"
#include "afxdialogex.h"


// CCreateJobDlg �Ի���

IMPLEMENT_DYNAMIC(CCreateJobDlg, CDialogEx)

CCreateJobDlg::CCreateJobDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_DIALOG_CREATE_JOB, pParent)
{

}

CCreateJobDlg::~CCreateJobDlg()
{
}

void CCreateJobDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CCreateJobDlg, CDialogEx)
	ON_BN_CLICKED(IDOK, &CCreateJobDlg::OnBnClickedOk)
END_MESSAGE_MAP()


// CCreateJobDlg ��Ϣ�������


void CCreateJobDlg::OnBnClickedOk()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	//CDialogEx::OnOK();
	CString cpages = _T("0");
	CString tbname = _T("NULL");
	GetDlgItemText(IDC_EDIT_TIEBANAME, tbname);
	GetDlgItemText(IDC_EDIT_TIEBAPAGE, cpages);
	int pg = _wtoi(cpages.GetBuffer());
	if (tbname == _T("") || pg < 1)
	{
		MessageBoxW(_T("��������Ч���ݣ�"), _T("����"), MB_ICONERROR | MB_OK);
		return;
	}
	pages = pg;
	tiebaName = tbname;
	CDialogEx::OnOK();
}
