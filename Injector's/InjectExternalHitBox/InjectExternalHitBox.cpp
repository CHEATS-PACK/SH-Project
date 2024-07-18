#include <windows.h>
#include <tlhelp32.h>
#include <iostream>

DWORD GetProcessId(const wchar_t* processName) {
    DWORD processId = 0;
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot != INVALID_HANDLE_VALUE) {
        PROCESSENTRY32 pe;
        pe.dwSize = sizeof(pe);
        if (Process32First(hSnapshot, &pe)) {
            do {
                if (wcscmp(pe.szExeFile, processName) == 0) {
                    processId = pe.th32ProcessID;
                    break;
                }
            } while (Process32Next(hSnapshot, &pe));
        }
        CloseHandle(hSnapshot);
    }
    return processId;
}

int main() {
    const wchar_t* dllPath = L"C:\\Windows\\vec.dll";
    const wchar_t* targetProcess = L"notepad.exe";

    DWORD processId = GetProcessId(targetProcess);
    if (!processId) {
        MessageBox(NULL, L"Не удалось найти процесс notepad.exe", L"Ошибка", MB_ICONERROR);
        return 1;
    }

    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
    if (!hProcess) {
        MessageBox(NULL, L"Не удалось открыть процесс notepad.exe", L"Ошибка", MB_ICONERROR);
        return 1;
    }

    void* pDllPathRemote = VirtualAllocEx(hProcess, NULL, (wcslen(dllPath) + 1) * sizeof(wchar_t), MEM_COMMIT, PAGE_READWRITE);
    if (!pDllPathRemote) {
        MessageBox(NULL, L"Не удалось выделить память в целевом процессе", L"Ошибка", MB_ICONERROR);
        CloseHandle(hProcess);
        return 1;
    }

    if (!WriteProcessMemory(hProcess, pDllPathRemote, (void*)dllPath, (wcslen(dllPath) + 1) * sizeof(wchar_t), NULL)) {
        MessageBox(NULL, L"Не удалось записать путь к DLL в память целевого процесса", L"Ошибка", MB_ICONERROR);
        VirtualFreeEx(hProcess, pDllPathRemote, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 1;
    }

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)LoadLibraryW, pDllPathRemote, 0, NULL);
    if (!hThread) {
        MessageBox(NULL, L"Не удалось создать удаленный поток в целевом процессе", L"Ошибка", MB_ICONERROR);
        VirtualFreeEx(hProcess, pDllPathRemote, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 1;
    }

    WaitForSingleObject(hThread, INFINITE);

    VirtualFreeEx(hProcess, pDllPathRemote, 0, MEM_RELEASE);
    CloseHandle(hThread);
    CloseHandle(hProcess);

    MessageBox(NULL, L"Инжектирование DLL успешно завершено!", L"Успех", MB_OK);

    return 0;
}
