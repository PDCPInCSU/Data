
// KCrawlerControal.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CKCCApp: 
// �йش����ʵ�֣������ KCrawlerControal.cpp
//

class CKCCApp : public CWinApp
{
public:
	CKCCApp();

// ��д
public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern CKCCApp theApp;