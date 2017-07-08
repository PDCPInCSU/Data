// KCCPlugins.cpp : ʵ���ļ�
//

#include "stdafx.h"
#include "KCrawlerControal.h"
#include "KCCPlugins.h"
#include "afxdialogex.h"
#include <locale.h>
#include "KCrawlerControalDlg.h"


// KCCPlugins �Ի���

IMPLEMENT_DYNAMIC(KCCPlugins, CDialogEx)

KCCPlugins::KCCPlugins(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_DIALOG_USE_PLUGINS, pParent)
{

}

KCCPlugins::~KCCPlugins()
{
	delete[] pluginlist;
}

void KCCPlugins::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_COMBO2, m_pluginslist);
}

//�ú���Ϊ�ϰ��������������Ѿ������ã�������δ���İ汾��������ʧ��
void KCCPlugins::loadPlugins()
{
	CStdioFile cfg;
	char* old_locale = _strdup(setlocale(LC_CTYPE, NULL));
	setlocale(LC_CTYPE, "chs");//�趨<ctpye.h>���ַ�����ʽ
	cfg.Open(PATH_PLUGINS_INDEX_FILE, CFile::modeRead);
	CString line = _T("");
	int pluginscount = 0;
	//�������
	while (cfg.ReadString(line))
	{
		//����ɣ�KCCPLUGINS=�����=������=����ļ���
		if (line.Find(_T("KCCPLUGINS")) >= 0)
		{
			pluginscount++;
		}
		line = _T("");
	}
	if (pluginscount < 1)
	{
		MessageBox(_T("δ�ҵ��κο��ò����������޷������κ����ݷ���������"), _T("����"), MB_ICONERROR | MB_OK);
		cfg.Close();
		return;
	}
	cfg.SeekToBegin();
	pluginlist = new Plugin[pluginscount];
	//ѭ�����ز��
	int i = 0;
	while (cfg.ReadString(line))
	{
		//��������ṹ��ÿһ�д���һ�����
		//����ɣ�KCCPLUGINS=�����=������=����ļ���
		if (line.Find(_T("KCCPLUGINS")) >= 0)
		{
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString name = line.Left(line.Find(_T("=")));
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString descri = line.Left(line.Find(_T("=")));
			line = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
			CString exefilename = line;
			if (exefilename.GetLength() < 3 || name.GetLength() == 0)
			{
				continue;
			}
			CString liststr = name + _T("->") + descri;
			m_pluginslist.AddString(liststr);
			//��������Ϣ��һ�����з���ִ��
			pluginlist[i].name = name;
			pluginlist[i].descri = descri;
			pluginlist[i].exefilename = exefilename;
			i++;
		}
		line = _T("");
	}
	setlocale(LC_CTYPE, old_locale);
	free(old_locale);//��ԭ�����趨
	cfg.Close();
}

void KCCPlugins::setupBasicInfo()
{

}

CString KCCPlugins::SearchPlugs()
{
	CFileFind finder;
	BOOL bWorking = finder.FindFile(_T(".\\plugins\\*.*"));
	CString pluginsData;
	while (bWorking)
	{
		bWorking = finder.FindNextFile();
		if (finder.IsDots())
			continue;
		CString foldername = (LPCTSTR)finder.GetFileName();
		//MessageBox(foldername);
		//�����Ͻ���������ļ������棬���ԣ���������Ҫ�ж��ǲ����ļ���
		if (finder.IsDirectory())
		{
			//MessageBox(_T("����main.py"), _T("����Ŀ¼..."), MB_ICONINFORMATION);
			CFileFind findmain;
			CString mainpath = _T(".\\plugins\\") + foldername + _T("\\main.py");
			if (findmain.FindFile(mainpath))
			{
				//��ȡ�����Ϣ�������Ϣ������3���ֶζ��壬������main.py�ļ�����
				//KCC_PLUGIN_NAME�������˲������
				//KCC_PLUGIN_DESCRIPTION�������˲������
				//KCC_PLUGIN_COPYRIGHT�������˲�������Լ���Ȩ��Ϣ
				CStdioFile readinfo;
				readinfo.Open(mainpath, CFile::modeRead);
				//MessageBox(_T("XXXXXXXXXXXXXXXXXXXX"), _T("�ҵ����ò��"), MB_ICONINFORMATION);
				CString line;
				CString NAME = foldername, DES = _T(""), CR=_T("δ֪����");
				int findcount = 0;
				while (readinfo.ReadString(line))
				{
					CKCCDlg kccdlg;
					line = kccdlg.UTF8_TO_GBK((char*)line.GetBuffer(0));
					if (findcount == 3)
					{
						break;
					}
					if (line.Find(_T("KCC_PLUGIN_NAME")) >= 0)
					{
						NAME = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
					if (line.Find(_T("KCC_PLUGIN_DESCRIPTION")) >= 0)
					{
						DES = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
					if (line.Find(_T("KCC_PLUGIN_COPYRIGHT")) >= 0)
					{
						CR = line.Right(line.GetLength() - line.Find(_T("=")) - 1);
						findcount++;
					}
				}
				pluginsData += NAME + _T("=") + DES + _T("=") + CR + _T("=") + foldername + _T("\\main.py#");
				readinfo.Close();
			}
		}
	}

	//���������ϣ���Ϣ��������pluginsData��
	return pluginsData;
}

void KCCPlugins::LoadPluginsNV()
{
	CString pluginsData = SearchPlugs();
	///MessageBox(pluginsData);
	int pluginscount = 0;
	for (int i = 0; i < pluginsData.GetLength(); i++)
	{
		if (pluginsData[i] == CString(_T("#")))
		{
			pluginscount++;
		}
	}
	pluginlist = new Plugin[pluginscount];
	for (int i = 0; i < pluginscount; i++)
	{
		CString NAME, DES, CP, PATH;
		NAME = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		DES = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		CP = pluginsData.Left(pluginsData.Find(_T("=")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("=")) - 1);
		PATH = pluginsData.Left(pluginsData.Find(_T("#")));
		pluginsData = pluginsData.Right(pluginsData.GetLength() - pluginsData.Find(_T("#")) - 1);
		//������Ϣ�������з���ִ��
		pluginlist[i].name = NAME;
		pluginlist[i].descri = DES;
		pluginlist[i].exefilename = PATH;
		//��ӵ��б����
		CString liststr = NAME + _T("->") + DES;
		m_pluginslist.AddString(liststr);
	}


}



BEGIN_MESSAGE_MAP(KCCPlugins, CDialogEx)
	ON_BN_CLICKED(IDC_ON_EXCUTE_PLUGINGS, &KCCPlugins::OnBnClickedOnExcutePlugings)
END_MESSAGE_MAP()


// KCCPlugins ��Ϣ�������


BOOL KCCPlugins::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// TODO:  �ڴ���Ӷ���ĳ�ʼ��
	LoadPluginsNV();
	setupBasicInfo();

	return TRUE;  // return TRUE unless you set the focus to a control
				  // �쳣: OCX ����ҳӦ���� FALSE
}


void KCCPlugins::OnBnClickedOnExcutePlugings()
{
	// TODO: �ڴ���ӿؼ�֪ͨ����������
	//�ж�ѡ����
	int selected = m_pluginslist.GetCurSel();
	if (selected < 0)
	{
		MessageBox(_T("δѡ���κο��ò����"), _T("����"), MB_ICONERROR | MB_OK);
		return;
	}
	CString exefilename = pluginlist[selected].exefilename;
	TCHAR currentDir[MAX_PATH];
	GetCurrentDirectory(MAX_PATH,currentDir);
	CString dir = currentDir;
	exefilename = _T("/C python " + dir + "\\plugins\\") + exefilename;
	//����python�ű�
	ShellExecute(NULL, _T("open"),_T("cmd.exe"), exefilename, NULL, SW_SHOW);
}
