handle_remove_scout( event_object );
handle_save_scout( event_object );

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

	// And the edit buttons
	$( '.scout_edit_button' ).button().unbind().click( handle_edit_scout );
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

// Converts the given target from a simple field containing text to an editable box with the new given id
function convert_to_field( target, new_id )
{
	var temp_contents = target.html();
	target.empty().append( '<input type="text" size="10" value="' + temp_contents + '" id="' + new_id + '"/>' );
}

function handle_edit_scout( event_object )
{
	var token = "edit_scout_";
	var scout_id = event_object.currentTarget.id.substring( token.length );

	// Get the row we are interested in
	var row_id = '#scout_row_' + scout_id;
	
	// Set up the edit boxes for first and last name
	var first_name = $( row_id + ' td:nth-child(2)' );
	convert_to_field( first_name, 'edit_first_name' );

	var last_name = $( row_id + ' td:nth-child(3)' );
	convert_to_field( last_name, 'edit_last_name' );

	// Set up the den dropdown box
	var den = $( row_id + ' td:nth-child(4)' );
	var temp = den.html();
	den.empty().append( '<select size="5" id="edit_den"></select>' );
	var dens = [ 'Tiger', 'Wolf', 'Bear', 'WeBeLoS' ];
	var selector = $( '#edit_den' );
	for( i in dens )
	{
		// Make sure that we pre-select the already-chosen value
		if( temp == dens[i] )
			selector.append( '<option value="' + dens[i] + '" selected>' + dens[i] + '</option>' );
		else
			selector.append( '<option value="' + dens[i] + '">' + dens[i] + '</option>' );
	}

	// Set up the birthday datepicker
	var birthday = $( row_id + ' td:nth-child(5)' );
	var temp = birthday.html();
	birthday.empty().append( '<input type="text" size="10" value="' + temp + '" id="edit_birthday" />' );
	$( '#edit_birthday' ).datepicker({ dateFormat:'yy-mm-dd' });
	
	// Alter the edit button to be a save button
	var edit_button = $( row_id + ' td:nth-child(6) :button' ).unbind().click( handle_save_scout );
	edit_button.empty().append( 'Save' );

	// Add a hidden id field
	$( row_id ).append( '<input type="hidden" id="edit_scout_id" value="' + scout_id + '"/>' );

}

function handle_save_scout( event_object )
{
	// Get all the values that are in the various fields
	var first_name = $( '#edit_first_name' ).val();
	var last_name = $( '#edit_last_name' ).val();
	var birthday = $( '#edit_birthday' ).val();
	var den_type = $( '#edit_den' ).val();
	var scout_id_field = $( '#edit_scout_id' );
	var scout_id = scout_id_field.val();
	scout_id_field.remove();

	event_object.currentTarget.innerHTML = 'Edit';

	Dajaxice.CubTrax.edit_scout( 'exit_edit_mode', {'scout_id':scout_id, 'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'den_type':den_type} );
}

function exit_edit_mode(data)
{
	$( '#edit_first_name' ).parent().empty().append( data.first_name );
	$( '#edit_last_name' ).parent().empty().append( data.last_name );
	$( '#edit_birthday' ).parent().empty().append( data.birthday );
	$( '#edit_den' ).parent().empty().append( data.den_type );

	setup_buttons();
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
	var new_row = '<tr id="scout_row_' + data.scout_id + '"><td><img width="50" height="50" src="' + STATIC_URL + 'CubTrax/img/avatar.jpg"/></td><td>' + data.first_name + "</td><td>" + data.last_name + "</td><td>" + data.den_type + "</td><td>" + data.birthday + '</td><td><button class="scout_edit_button button" id="edit_scout_' + data.scout_id + '">Edit</button></td><td><button class="scout_delete_button button" id="delete_scout_' + data.scout_id + '">X</button></td></tr>';

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
