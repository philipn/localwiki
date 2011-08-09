(function()
{
	function addPluginsButton( editor )
	{
		var menuGroup = 'wikipluginsButton';
		editor.addMenuGroup( menuGroup );
		var menuItems = editor.config.wikiplugins_menu;
		jQuery.each(menuItems, function(itemName, item){
			item.group = menuGroup;
		});

		editor.addMenuItems( menuItems );
		editor.ui.add( 'Plugins', CKEDITOR.UI_MENUBUTTON,
			{
				label : 'Insert Object',
				title : 'Insert Object',
				className : 'cke_button_plugins',
				modes : { wysiwyg : 1 },
				onRender: function()
				{
					// TODO: hook up custom plugins?
				},
				onMenu : function()
				{
					var states = {};
					jQuery.each(menuItems, function(itemName){
						states[itemName] = CKEDITOR.TRISTATE_OFF;
					});
					return states;
					// TODO: turn buttons on/off depending on selection
				}
			});
	}

	CKEDITOR.plugins.add( 'wikiplugins',
	{
		requires : [ 'menubutton' ],
		beforeInit : function( editor )
		{
			editor.config.wikiplugins_menu = {};
		},
		init : function( editor )
		{
			addPluginsButton( editor );
		}
	});
})();
