# EstimateXtract_AI

Project Goal:
Develop an AI-powered system to extract and reformat data from various PDF project estimates for windows and doors. The system should:
1. Extract relevant data from PDFs with different layouts and formats.
2. Apply rules to group and reorganize the data into a user-friendly format.
3. Identify common denominators and create headers for each group.
4. Display only the differences between similar items (e.g., window sizes, owners) as line items below each header.
5. Automate the process using AI, enabling the system to self-learn and understand the data structure.
Additional Requirements:
- Implement rules-based system to prompt users to override certain descriptions with more user-friendly terms, such as:
- Mapping technical terms to simpler descriptions (e.g., "Black encoded" to "Black").
- Replacing manufacturer-specific names with standardized terms.
- Allow users to maintain a mapping dictionary to override vendor descriptions with their preferred terms.
- Enable users to update and refine the mapping dictionary as needed.
Input:
- PDF project estimates from various manufacturers with different layouts and formats.
- Each PDF contains specs for windows and doors, with repeated information for similar items.
Output:
- A reformatted document with:
- Headers grouping common specs for similar items (e.g., window type, material).
- Line items displaying only the differences between similar items (e.g., size, owner).
- User-friendly descriptions replacing technical terms and manufacturer-specific names.
Key Requirements:
- AI-powered data extraction and reformatting.
- Ability to handle different PDF layouts and formats.
- Automatic grouping and header creation based on common denominators.
- User-friendly output format for easy comparison and analysis.
- Rules-based system for prompting user overrides.
- User-maintained mapping dictionary for term standardization.
