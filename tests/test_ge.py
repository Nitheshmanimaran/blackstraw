import great_expectations as gx
from great_expectations.exceptions import DataContextError

def test_ge_configuration():
    try:
        # Initialize the GE context
        context = gx.get_context()

        # Load the checkpoint configuration
        checkpoint_name = "my_checkpoint"
        checkpoint = context.get_checkpoint(checkpoint_name)

        # Run the checkpoint
        checkpoint_result = checkpoint.run()

        # Check if the validation was successful
        if checkpoint_result["success"]:
            print("Data quality check passed.")
        else:
            print("Data quality check failed.")
            for validation_result in checkpoint_result["run_results"].values():
                if not validation_result["validation_result"]["success"]:
                    print(validation_result["validation_result"])

        # Build and open Data Docs
        context.build_data_docs()
        validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]
        context.open_data_docs(resource_identifier=validation_result_identifier)

    except DataContextError as e:
        print(f"Error loading GE context: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_ge_configuration()