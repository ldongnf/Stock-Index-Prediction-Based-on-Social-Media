@echo 现在清除Cookies
@Rundll32 InetCpl.cpl,ClearMyTracksByProcess 2
@echo 现在清除浏览历史
@Rundll32 InetCpl.cpl,ClearMyTracksByProcess 1
@echo 现在清除临时文件夹
@Rundll32 InetCpl.cpl,ClearMyTracksByProcess 8
@echo 现在清除保存的密码
@Rundll32InetCpl.cpl,ClearMyTracksByProcess 32
@echo 现在清除表单数据
@Rundll32 InetCpl.cpl,ClearMyTracksByProcess 16
@echo 现在清除以上所有项目
@Rundll32 InetCpl.cpl,ClearMyTracksByProcess 255echo