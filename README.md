# mac2oui Analyzer

This analyzer resolves the organization for a mac address.

This is a [Cortex-Analyzer](https://github.com/TheHive-Project/Cortex-Analyzers).

The analyzer is for the observable type `mac`, which has to be added in TheHive manually.

The analyzer requires a database for the oui-company-mapping. You can get this database from the [IEEE](http://standards-oui.ieee.org/oui/oui.csv).
You can place the database anywhere, but you have to configure the path. The recommended place is in the mac2ouiAnalyzer folder, it is the default path in the settings.

The html templates (mac2ouiAlanyzer_1_0 folder) has to be placed in the thehive-templates folder.