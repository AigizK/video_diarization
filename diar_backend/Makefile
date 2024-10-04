APP_NAME=diar-backend

SERVICE=$(APP_NAME).service
HOST_DIR=/root/proj/video_diarization/video_diarization/diar_backend

.PHONY: install
enable:
	ssh -t $(HOST) sudo systemctl enable $(HOST_DIR)/$(SERVICE)
.PHONY: start
start:
	ssh -t $(HOST) sudo systemctl daemon-reload
	ssh -t $(HOST) sudo systemctl start $(SERVICE)

.PHONY: stop
stop:
	ssh -t $(HOST) sudo systemctl stop $(SERVICE)

.PHONY: logs
logs:
	ssh -t $(HOST) sudo journalctl -u $(SERVICE) -f

