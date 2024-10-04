APP_NAME=diar-backend

SERVICE=$(APP_NAME).service
HOST_DIR=/root/proj/video_diarization/video_diarization/diar_backend

.PHONY: install
enable:
	sudo systemctl enable $(HOST_DIR)/$(SERVICE)
.PHONY: start
start:
	sudo systemctl daemon-reload
	sudo systemctl start $(SERVICE)

.PHONY: stop
stop:
	sudo systemctl stop $(SERVICE)

.PHONY: logs
logs:
	sudo journalctl -u $(SERVICE) -f

