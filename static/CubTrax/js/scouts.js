handle_remove_scout( event_object );

function setup_scout_page()
{
	// Stripe the table
	stripe_tables();

	// Setup the add scout dialog
	$( "#add_scout_dialog" ).dialog({
			title: 'Add a scout',
			minWidth: 390,
			autoOpen: false,
			show: "blind",
			hide: "explode"
		});

	// Take care of the add scout button
	$( '#add_scout_popup_button' ).button().click( popup_add_scout_dialog );
	$( "#add_scout_button" ).button().click( handle_add_scout );
	$( "#new_scout_birthday" ).datepicker({
		defaultDate: '-8y',
		dateFormat: 'yy-mm-dd'
	});

	setup_buttons();
};

function setup_buttons()
{
	// Take care of the remove buttons
	$( '.scout_delete_button' ).button().unbind().click( handle_remove_scout );
}

function handle_remove_scout( event_object )
{
	if( confirm( "Delete?" ) )
	{
		var token = "delete_scout_";
		var scout_id = event_object.currentTarget.id.substring( token.length );
	
		Dajaxice.CubTrax.remove_scout( 'remove_from_scout_table', {'scout_id':scout_id} );
	}
}

function handle_add_scout()
{
	$( '.add_scout_widget' ).attr('disabled', true);

	var first_name = $( '#new_scout_first_name' ).val();
	var last_name = $( '#new_scout_last_name' ).val();
	var birthday = $( '#new_scout_birthday' ).val();
	var den_type = $( '#new_scout_den_type' ).val();

	Dajaxice.CubTrax.add_scout( 'add_to_scout_table', {'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'den_type':den_type});
};

function popup_add_scout_dialog()
{
	$( "#add_scout_dialog" ).dialog( "open" );
};

function add_to_scout_table(data)
{
	$( '#new_scout_first_name' ).val('');
	$( '#new_scout_last_name' ).val('');
	$( '#new_scout_birthday' ).val('');

	// Hide the dialog
	$( '#add_scout_dialog' ).dialog('close');

	// Add a new row
	var new_row = '<tr id="scout_row_' + data.scout_id + '"><td><img width="50" height="50" src="' + STATIC_URL + 'CubTrax/img/avatar.jpg"/></td><td>' + data.first_name + "</td><td>" + data.last_name + "</td><td>" + data.den_type + "</td><td>" + data.birthday + '</td><td><button class="scout_delete_button button" id="delete_scout_' + data.scout_id + '">X</button></td></tr>';

	$( "#scout_table tr:last" ).after( new_row );

	// Set up the delete button
	setup_buttons();

	// Highlight the new row
	$( '#scout_table tr:last' ).effect('highlight');

	// Re-color the rows
	stripe_tables();

	$( '.add_scout_widget' ).attr('disabled', false);

};

function remove_from_scout_table(data)
{
	$( '#scout_row_' + data.scout_id ).remove();

	stripe_tables();
}
