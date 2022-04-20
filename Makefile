PYTHON_INTERPRETER = python3
PROJECT_NAME = search
ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

create_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python=3.8 --file requirements.txt -y
endif
		@echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
endif

remove_environment:
	conda env remove --name $(PROJECT_NAME)