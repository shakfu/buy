all: build


build:
	-@swift build -Xlinker -L/usr/local/lib


release:
	-@swift build -c release -Xlinker -L/usr/local/lib


format:
	-@swift-format --configuration .swiftformatrc --recursive --in-place ./src


clean:
	-@rm -rf .build
