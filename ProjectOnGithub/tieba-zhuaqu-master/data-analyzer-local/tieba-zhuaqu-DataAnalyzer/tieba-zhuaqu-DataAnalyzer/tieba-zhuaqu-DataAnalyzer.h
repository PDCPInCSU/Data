
// tieba-zhuaqu-DataAnalyzer.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CDAApp: 
// �йش����ʵ�֣������ tieba-zhuaqu-DataAnalyzer.cpp
//

class CDAApp : public CWinApp
{
public:
	CDAApp();

// ��д
public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern CDAApp theApp;