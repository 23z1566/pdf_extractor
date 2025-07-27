@echo off
echo Running Collection 1
docker run --rm ^
  -v "%cd%\Collection 1\PDFs:/app/input" ^
  -v "%cd%\Collection 1\challenge1b_input.json:/app/challenge1b_input.json" ^
  -v "%cd%\Collection 1:/app/output" ^
  adobe1b

echo Running Collection 2
docker run --rm ^
  -v "%cd%\Collection 2\PDFs:/app/input" ^
  -v "%cd%\Collection 2\challenge1b_input.json:/app/challenge1b_input.json" ^
  -v "%cd%\Collection 2:/app/output" ^
  adobe1b

echo Running Collection 3
docker run --rm ^
  -v "%cd%\Collection 3\PDFs:/app/input" ^
  -v "%cd%\Collection 3\challenge1b_input.json:/app/challenge1b_input.json" ^
  -v "%cd%\Collection 3:/app/output" ^
  adobe1b

echo All collections processed successfully!
pause
